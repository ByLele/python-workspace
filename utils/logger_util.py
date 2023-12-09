from loguru import logger
import sys
#格式化日志
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
) 

#日志保存
logger.add(
    'info.log',
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {module}:{function}:{line} - {message}",
    level="INFO",
)
#日志轮换
logger.add("debug.log", level="INFO", rotation="1 week", retention="4 weeks")

#日志过滤

#logger.add("test.log", filter=lambda x: "Cai Xukong" in x["message"], level="INFO")
