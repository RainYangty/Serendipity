import logging
import sys

def log_write(a, txt):
    """
    :param a: 日志类型 info || warning
    :param txt: 日志内容
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.INFO)
    path = str(sys.argv[0])[:-14] + "log.log"
    handler = logging.FileHandler(path)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if(a == "info"):
        logger.info(txt)
    if(a == "warning"):
        logger.warning(txt)
    logger.removeHandler(handler)  # 日志写入完成后移除handler From: https://blog.csdn.net/Ximerr/article/details/114677224