import time
import spacy
import queue
import multiprocessing
from .utils import cleanup_document
from .logger import get_logger
from .configurations.config import ConfigParser
from .node_models import Topic, Document, Entity
nlp = spacy.load("en_core_web_sm")

config_obj =ConfigParser()
num_processes = config_obj.num_process
queue_timeout = config_obj.queue_timeout
log_file_path = config_obj.log_file_path
logger = get_logger(log_file_path)


def write_to_graph(out_queue):
    pass


def process_document(in_queue, out_queue):
    pass

def read_documents(in_queue):
    pass


def handle_error(e):
    print(e)

if __name__ == '__main__':
    input_queue = multiprocessing.Manager().Queue()
    output_queue = multiprocessing.Manager().Queue()

    pool = multiprocessing.Pool(num_processes)
    #module to read the news feed file
    pool.apply_async(read_documents, (input_queue, ), error_callback=handle_error)
    time.sleep(10)
    #module to process a news article
    jobs = [pool.apply_async(process_document, (input_queue, output_queue)) for i in range(num_processes - 2)]
    #modules to update neo4j graph with appropriate nodes and relationship
    pool.apply_async(write_to_graph, (output_queue, ))
    pool.close()
    pool.join()