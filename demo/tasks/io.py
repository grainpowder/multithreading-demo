import asyncio
import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Tuple

import httpx

from util import make_logger

URL_LIST = [
   "https://amazon.com",
   "https://apple.com",
   "https://facebook.com",
   "https://github.com",
   "https://google.com",
   "https://instagram.com",
   "https://naver.com",
   "https://samsung.com",
] * 3


class SynchronousIOBoundTask:
    logger = make_logger("sync")

    @staticmethod
    def fetch(client: httpx.Client, url: str, warmup: bool) -> httpx.Response:
        response = client.get(url, follow_redirects=True)

        pid = os.getpid()
        tid = threading.get_ident()
        status_code = response.status_code
        if not warmup:
            SynchronousIOBoundTask.logger.info(f"PID : {pid}, TID : {tid}, status : {status_code}, url : {url}")

        return response

    @staticmethod
    def execute(warmup: bool):
        with httpx.Client() as client:
            start = time.time()
            result = [SynchronousIOBoundTask.fetch(client, url, warmup) for url in URL_LIST]
            if not warmup:
                SynchronousIOBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f} seconds")


class MultithreadIOBoundTask:
    logger = make_logger("multithread")

    @staticmethod
    def fetch(parameter: Tuple[httpx.Client, str]) -> httpx.Response:
        client, url = parameter
        response = client.get(url, follow_redirects=True)

        pid = os.getpid()
        tid = threading.get_ident()
        status_code = response.status_code
        MultithreadIOBoundTask.logger.info(f"PID : {pid}, TID : {tid}, status : {status_code}, url : {url}")

        return response

    @staticmethod
    def execute():
        with httpx.Client() as client:
            start = time.time()
            params = [(client, url) for url in URL_LIST]
            executor = ThreadPoolExecutor(max_workers=5)
            result = list(executor.map(MultithreadIOBoundTask.fetch, params))
            MultithreadIOBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f} seconds")


class AsynchronousIOBoundTask:
    logger = make_logger("async")

    @staticmethod
    async def fetch(client: httpx.AsyncClient, url: str) -> httpx.Response:
        response = await client.get(url, follow_redirects=True)

        pid = os.getpid()
        tid = threading.get_ident()
        status_code = response.status_code
        AsynchronousIOBoundTask.logger.info(f"PID : {pid}, TID : {tid}, status : {status_code}, url : {url}")

        return response

    @staticmethod
    async def execute():
        """
        :: Equivalent codes ::
        1. result = await asyncio.gather(fetch(client, URL_LIST[0]), fetch(client, URL_LIST[1]), ...)
         -> asyncio.gather의 각 인자는 awaitable 객체여야 하고, 리스트는 awaitable하지 않기 때문에 언패킹 필요
        2. client = httpx.AsyncClient()
           result = await asyncio.gather(*[fetch(client, url) for url in URL_INFO])
           await client.aclose()
         -> 세션은 작업이 끝나면 종료해줘야 한다는게 핵심
        """
        async with httpx.AsyncClient() as client:
            start = time.time()
            result = await asyncio.gather(*[AsynchronousIOBoundTask.fetch(client, url) for url in URL_LIST])
            AsynchronousIOBoundTask.logger.info(f"Elapsed time : {time.time() - start:.4f} seconds")
