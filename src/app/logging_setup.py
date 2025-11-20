import logging
from logging.handlers import TimedRotatingFileHandler
from .utils.paths import logs_dir

def setup_logging(level="INFO"):
    log_file = logs_dir() / "app.log"
    fmt = "%(asctime)s | %(levelname)-8s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Consola
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(fmt, datefmt))
    root.addHandler(ch)

    # Archivo rotativo
    fh = TimedRotatingFileHandler(str(log_file), when="D", interval=7, backupCount=4, encoding="utf-8")
    fh.setFormatter(logging.Formatter(fmt, datefmt))
    root.addHandler(fh)