import logging
import sys
from enum import Enum


class BoundType(Enum):
    CPU = "cpu"
    IO = "io"


def make_logger(logger_name: str) -> logging.Logger:
    # 각 handler에서 사용할 로그 형식 정의
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(msg)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 콘솔 출력을 위한 handler 정의
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # logger를 만들고 앞서 정의한 handler 추가
    logger = logging.getLogger(logger_name)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger
