import time
import spacy
import queue
import gensim
import multiprocessing
from logger import get_logger
import gensim.corpora as corpora
from neomodel import config
from configurations.config import ConfigParser
from node_models import Topic, Document, Entity
from utils import cleanup_document, populate_topics_in_neo4j
nlp = spacy.load("en_core_web_sm")

config_obj =ConfigParser()
num_processes = config_obj.num_process
queue_timeout = config_obj.queue_timeout
log_file_path = config_obj.log_file_path
model_path = config_obj.topic_model_path
logger = get_logger(log_file_path)

# DB url for neo4j
config.DATABASE_URL = config_obj.neo4j_url

def write_to_graph(out_queue):
    pass


def process_article(in_queue, out_queue):
    pass

def read_documents(in_queue):
    pass


def handle_error(e):
    print(e)


def process_news_feed():
    input_queue = multiprocessing.Manager().Queue()
    output_queue = multiprocessing.Manager().Queue()

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


if __name__ == '__main__':
    populate_topics_in_neo4j(model_path, logger)
    # process_news_feed()
