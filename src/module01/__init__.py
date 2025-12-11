from src.utils.logger import init_logger

module_name = "module01"

logger = init_logger()
logger.bind(module=module_name)
