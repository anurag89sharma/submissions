import os
import configparser


class Singleton(type):
    '''Singleton Meta class'''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigParser(metaclass=Singleton):
    '''Configuration class for serving data'''

    def __init__(self):
        config = configparser.RawConfigParser()
        current_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_path, 'config.ini')
        config.readfp(open(file_path))

        self.version = config.get('Version', 'VERSION')
        self.log_directory = config.get('Log Path', 'LOG_DIRECTORY')
        self.environment = config.get('ENVIRONMENT', 'ENV')

        self.db_name = config.get('MongoDb Config', 'DB_NAME')
        self.db_alias = config.get('MongoDb Config', 'DB_ALIAS')
        self.mongo_db_hostname = config.get('MongoDb Config', 'MONGO_DB_HOSTNAME')
        self.mongo_db_port = config.get('MongoDb Config', 'MONGO_DB_PORT')
        self.replica_set_name = config.get('MongoDb Config', 'REPLICA_SET_NAME')
        self.mongo_connection_url = config.get('MongoDb Config', 'CONNECTION_URL')

    def get_mongo_replica_set_name(self):
        return self.replica_set_name

    def get_mongo_db_connection_uri(self):
        return self.mongo_connection_url % (self.mongo_db_hostname, self.mongo_db_port, self.db_name)
