import re
import json
import spacy
import gensim
from pprint import pprint
from bs4 import BeautifulSoup
from node_models import Topic, Keyword
from logger import get_basic_logger
from gensim.parsing.preprocessing import STOPWORDS


def get_topics(document, lda_model, spacy_model):
    cleaned_text = topic_level_cleaning(document, spacy_model)
    corpus = lda_model.id2word.doc2bow(cleaned_text)
    topics = lda_model[corpus]
    # topics = sorted(topics, key=lambda x: (x[1]), reverse=True)
    # print(len(corpus), len(second_pass))
    return topics


def get_entities_from_spacy(document, spacy_model):
    cleaned_text = entity_level_cleaning(document)
    doc = spacy_model(cleaned_text)
    # ignore entities having length less than4 and greater than 30
    return {(X.text.lower().title(), X.label_) for X in doc.ents
            if X.label_ in {'PERSON', 'ORG', 'GPE'} and  4 < len(X.text) <= 30}


def basic_cleanup(document):
    # Function to convert a document to a sequence of words,

    # 1. Remove HTML
    soup = BeautifulSoup(document, 'html5lib') # create a new bs4 object from the html data loaded
    for script in soup(["script", "style", "form"]): # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()

    return text


def topic_level_cleaning(text, spacy_model):
    allowed_postags = ['NOUN', 'ADJ', 'VERB', 'ADV']

    # 1. Remove non-letters
    review_text = re.sub("[^a-zA-Z]", " ", text)
    review_text = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', review_text)

    # 2. convert to lower case
    review_text = review_text.lower()

    # 3. Replace multiple spaces with single space
    document = re.sub(' +', ' ', review_text).strip()

    # 4. remove stopwords
    document = [word for word in document.split() if word not in STOPWORDS]

    #5. Lemmatize
    doc = spacy_model(" ".join(document))
    return [token.lemma_ for token in doc if token.pos_ in allowed_postags]


def entity_level_cleaning(document):
    # 1. Remove non-letters (preserving '.' char to know the ending of sentence)
    review_text = re.sub("[^a-zA-Z0-9.]", " ", document)
    # 2. Separate out thing like asp.net p.m with beginning of sentences
    review_text = re.sub("[.]", ". ", review_text)

    review_text = re.sub(r'([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))', r'\1 ', review_text)

    # conversion to lowercase is not checked as capitalization is required
    # for detection of entities like person, organization or location

    # 3. Replace multiple spaces with single space
    document = re.sub(' +', ' ', review_text).strip()
    return document


def populate_topics_in_neo4j(model_path, logger, num_words=25):
    lda_model = gensim.models.ldamodel.LdaModel.load(model_path)
    logger.info("Number of Topics - {}".format(lda_model.num_topics))
    topics = lda_model.show_topics(lda_model.num_topics, num_words=num_words, formatted=False)
    for topic in topics:
        topic_name, keywords = topic
        logger.info("Number of keywords for topic({}) is - {}".format(topic_name, len(keywords)))
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
    logger = get_basic_logger()
    nlp = spacy.load("en_core_web_sm")
    model_path = '/Users/anuragsharma/Work/submissions/logically/saved_model/lda_model_25topics_2passes.model'
    file_path = "/Users/anuragsharma/Work/submissions/logically/signalmedia-1m.jsonl"

    lda_model = gensim.models.ldamodel.LdaModel.load(model_path)

    with open(file_path) as fp:
        lines = fp.readlines()
        for i in range(10):
            document = basic_cleanup(json.loads(lines[i]).get('content'))
            # topics = get_topics(document, lda_model, nlp)
            # print(topics, "\n")

            entities = get_entities_from_spacy(document, nlp)
            pprint(entities)

