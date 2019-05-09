import re
import gensim
from bs4 import BeautifulSoup
from node_models import Topic, Keyword
from logger import get_basic_logger


def cleanup_document(document):
    # Function to convert a document to a sequence of words,

    # 1. Remove HTML
    soup = BeautifulSoup(document, 'html5lib') # create a new bs4 object from the html data loaded
    for script in soup(["script", "style", "form"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    review_text = soup.get_text()

    # 2. Remove non-letters (preserving '.' char to know the ending of sentence)
    review_text = re.sub("[^a-zA-Z.]", " ", review_text)
    review_text = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', review_text)

    # 4. Replace multiple spaces with single space
    document = re.sub(' +', ' ', review_text).strip()
    return document


def populate_topics_in_neo4j(model_path, logger):
    lda_model = gensim.models.ldamodel.LdaModel.load(model_path)
    logger.info("Number of Topics - {}".format(lda_model.num_topics))
    topics = lda_model.show_topics(lda_model.num_topics, formatted=False)
    for topic in topics:
        topic_name, keywords = topic
        logger.info("Creating graph node for topic - {}".format(topic_name))
        topic_node = Topic.get_or_create({"name": str(topic_name)})[0]
        for keyword in keywords:
            word, weight = keyword
            logger.info("Creating graph node for keyword - {}".format(word))
            keyword_node = Keyword.get_or_create({"name": word})[0]
            logger.info("Linking Topic node({}) with Keyword node({}) with weight - {}".
                        format(topic_name, word, weight))
            _ = topic_node.hasKeyword.connect(keyword_node, {"weight": weight})


if __name__ == '__main__':
    pass
