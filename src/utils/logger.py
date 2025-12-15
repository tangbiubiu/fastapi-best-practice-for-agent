import os
import sys
from loguru import logger

def init_logger():
    logger.remove()
    format_str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{extra[module]}</cyan> | "
        "<level>{message}</level>"
    )
    
    # 添加默认的 module 字段到所有日志记录
    logger.configure(extra={"module": "unknown"})
    
    if os.getenv("PROJECT_ENV") == "prod":
        logger.add(
            "logs/app_{time}.log",  # 保存log日志
            format=format_str,  # 定义log格式
            level="INFO",  # 显示log的最低级别
            rotation="10 MB",  # 滚动分割，最大10MB
            retention="30 days",  # 自动删除久于一个月的log
            compression="zip",  # 压缩格式
            enqueue=True
        )

        logger.add(
            "logs/error_{time}.log",
            format=format_str,
            level="ERROR",
            rotation="100 MB",
            retention="30 days",
            enqueue=True,
            filter=lambda record: record["level"].no >= 40  # ERROR及以上
        )
    else:
        logger.add(
            sys.stderr,  # 保存log日志
            format=format_str,  # 定义log格式
            level="DEBUG",  # 显示log的最低级别
        )

    return logger