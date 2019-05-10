import time
import json
import spacy
import queue
import gensim
import multiprocessing
from neomodel import config
from logger import get_logger
from nltk.tag import StanfordNERTagger
from configurations.config import ConfigParser
from node_models import Topic, Document, Entity
from utils import basic_cleanup, populate_topics_in_neo4j, get_topics, get_entities_from_nltk


config_obj =ConfigParser()
nlp = spacy.load("en_core_web_sm")
num_processes = config_obj.num_process
queue_timeout = config_obj.queue_timeout
log_file_path = config_obj.log_file_path
model_path = config_obj.topic_model_path
logger = get_logger(log_file_path)

# DB url for neo4j
config.DATABASE_URL = config_obj.neo4j_url


def write_to_graph(out_queue):
    topic_nodes = {}
    document_id = ""
    logger.info("Inside write to GraphDB method")
    while 1:
        try:
            write_payload = out_queue.get(True, queue_timeout)
            document_id = write_payload.get("document_id")
            topics = write_payload.get("topics")
            entities = write_payload.get("entities")

            document_node = Document.get_or_create({"documentId": document_id})[0]
            for topic_name, weight in topics:
                if topic_name in topic_nodes:
                    topic_node = topic_nodes[topic_name]
                else:
                    topic_node = Topic.get_or_create({"name": str(topic_name)})[0]
                    topic_nodes[topic_name] = topic_node

                logger.info("Linking document node - {} with topic node - {}".format(document_id, topic_name))
                _ = document_node.topic.connect(topic_node, {"weight": weight})

            for entity_name, entity_type in entities:
                key = "{}-{}".format(entity_name, entity_type.lower())
                logger.info("Linking document node - {} with entity node - {} of type {}".
                            format(document_id, entity_name, entity_type))
                entity_node = Entity.get_or_create(
                    {"name": entity_name, "entity_type": entity_type, "key": key})[0]
                _ = document_node.entity.connect(entity_node)

        except queue.Empty as e:
            logger.exception("Queue is empty. Quitting!!!")
            break
        except Exception as e:
            logger.exception("Exception Occurred in processing document-id - {}!!!".format(document_id))

    logger.info("Done Writing to Storage")


def process_article(in_queue, out_queue):
    document_id = ""
    logger.info("Processing of news feed started!!!")
    lda_model = gensim.models.ldamodel.LdaModel.load(model_path)
    stanford_tagger = StanfordNERTagger(config_obj.stanford_ner_classifier_path, config_obj.stanford_ner_jar_path)
    while 1:
        try:
            document = in_queue.get(True, queue_timeout)
            document_id, document_content = document.get('id'), document.get('content')
            if document_id:
                logger.info("Processing document id - {}".format(document_id))
                node = Document.nodes.get_or_none(documentId=document_id)
                if node:
                    logger.info("Node with id - {} already exists in graph. Skipping".format(document_id))
                    continue
                else:
                    cleaned_text = basic_cleanup(document_content)
                    topics = get_topics(cleaned_text, lda_model, nlp)
                    entities = get_entities_from_nltk(cleaned_text, stanford_tagger)

                    payload = {"document_id": document_id, "topics": topics, "entities": entities}
                    out_queue.put(payload, block=True)
            else:
                continue
        except queue.Empty as e:
            logger.warning("Queue is empty. Quitting!!!")
            break
        except Exception as e:
            logger.exception("Exception in processing %s, Skipping !!!!" % document_id)
    logger.info("Work done. Quitting")


def read_documents(in_queue):
    file_path = config_obj.news_feed_file_path
    logger.info("Started reading file - {}".format(file_path))
    with open(file_path) as fp:
        lines = fp.readlines()
        try:
            for index, line in enumerate(lines):
                if index==config_obj.num_documents:break
                document = json.loads(line)
                in_queue.put(document, block=True)
        except Exception as e:
            logger.exception("Exception Occurred!!!")

    logger.info("Done Fetching Records from path - {}".format(file_path))


def handle_error(e):
    print(e)


def process_news_feed():
    logger.info("Processing of news feed started!!!")
    t0 = time.time()
    input_queue = multiprocessing.Manager().Queue(1000000)
    output_queue = multiprocessing.Manager().Queue(1000000)

    pool = multiprocessing.Pool(num_processes)
    # module to read the news feed file
    pool.apply_async(read_documents, (input_queue,), error_callback=handle_error)
    time.sleep(10)
    # module to process a news article
    jobs = [pool.apply_async(process_article, (input_queue, output_queue)) for i in range(num_processes - 2)]
    # modules to update neo4j graph with appropriate nodes and relationship
    pool.apply_async(write_to_graph, (output_queue,))
    pool.close()
    pool.join()
    t1 = time.time()

    logger.info("News feed parsing took - {} seconds".format(round(t1-t0, 2)))


if __name__ == '__main__':
    # populate_topics_in_neo4j(model_path, logger)
    process_news_feed()
