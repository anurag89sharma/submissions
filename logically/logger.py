import sys
import logging
import traceback
import threading
import multiprocessing
from logging.handlers import RotatingFileHandler


class Singleton(type):
    '''Singleton Meta class'''
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


# ============================================================================
# Define Log Handler
# ============================================================================
class CustomLogHandler(logging.Handler, metaclass=Singleton):
    """
    multiprocessing log handler
    This handler makes it possible for several processes
    to log to the same file by using a queue.

    """
    def __init__(self, fname, status_code=None):
        logging.Handler.__init__(self)

        # self._handler = FH(fname)
        # Change log file after every 200MB of data pushed to the file
        self._handler = RotatingFileHandler(fname, maxBytes=200000000, backupCount=10)
        self.queue = multiprocessing.Queue(-1)

        thrd = threading.Thread(target=self.receive)
        thrd.daemon = True
        thrd.start()

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except EOFError:
                break
            except:
                traceback.print_exc(file=sys.stderr)

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            dummy = self.format(record)
            record.exc_info = None

        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)


def get_logger(file_path="/mnt/resource/logs/job_logs.out"):
    logger = logging.getLogger(__name__)
    handler = CustomLogHandler(file_path)
    formatter = logging.Formatter(
        '[%(asctime)s - %(filename)s - %(processName)s] - %(lineno)d - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

def get_basic_logger():
    logging.basicConfig(
        format='[%(asctime)s - %(filename)s - %(processName)s] - %(lineno)d - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    return logger

if __name__ == "__main__":
    logger = get_logger("/backup/job_logs.out")


    logger.info("Hello World")
