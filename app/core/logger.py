import logging
import uuid

from elasticapm.handlers.logging import Formatter, LoggingFilter

LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_root_logger():
    logger_ = logging.getLogger('elasticapm')
    if logger_.hasHandlers():
        logger_.handlers.clear()
    formatter = Formatter(LOG_FORMAT)
    console = logging.StreamHandler()
    console.addFilter(LoggingFilter())
    console.setFormatter(formatter)
    logger_.addHandler(console)
    logger_.setLevel(logging.INFO)

    factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = factory(*args, **kwargs)
        record.request_id = uuid.uuid4()
        return record

    logging.setLogRecordFactory(record_factory)


LOG_DEFAULT_HANDLERS = ['console']

logger = logging.getLogger('elasticapm')
