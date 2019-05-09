import os
import configparser


class ConfigParser():

    def __init__(self):
        config = configparser.RawConfigParser()
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_path, 'config.ini')
        config.readfp(open(file_path))

        self.version = config.get('Parameters', 'VERSION')
        self.neo4j_url = config.get('Neo4j', 'NEO4J_URL')
        self.topic_model_path = config.get('Topic Model', 'MODEL_PATH')
        self.num_process = config.get('Parser', 'PROCESS_TO_FORK')
        self.queue_timeout = config.get('Parser', 'QUEUE_TIMEOUT_LIMIT')
        self.num_documents = config.get('News Feed', 'NUM_DOCS_TO_PROCESS')
        self.news_feed_file_path = config.get('News Feed', 'FILE_PATH')
        self.log_file_path = config.get('Logging', 'LOG_FILE_PATH')
