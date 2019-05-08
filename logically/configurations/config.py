import os
import configparser


class ConfigParser():

    def __init__(self):
        config = configparser.RawConfigParser()
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_path, 'config.ini')
        config.readfp(open(file_path))

        self.version = config.get('Parameters', 'VERSION')
        self.neo4j_url = config.get('Parameters', 'NEO4J_URL')
        self.num_process = config.get('Parameters', 'PROCESS_TO_FORK')
        self.queue_timeout = config.get('Parameters', 'QUEUE_TIMEOUT_LIMIT')
        self.num_documents = config.get('Parameters', 'NUM_DOCS_TO_PROCESS')
        self.log_file_path = config.get('Parameters', 'LOG_FILE_PATH')