import time
import spacy
import queue
import multiprocessing
from .config import *
from .utils import cleanup_document
from .node_models import Topic, Document, Entity


nlp = spacy.load("en_core_web_sm")

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
    num_processes = PROCESS_TO_FORK

    pool = multiprocessing.Pool(num_processes)
    num_readers = 1
    readers = pool.apply_async(read_documents, (input_queue, ), error_callback=handle_error)
    time.sleep(10)
    jobs = [pool.apply_async(process_document, (input_queue, output_queue)) for i in range(num_processes - 2)]
    pool.apply_async(write_to_graph, (output_queue, ))
    pool.close()
    pool.join()