import requests
from requests.sessions import Session
from concurrent.futures import ThreadPoolExecutor
from threading import local
from loguru import logger


class LinkDownloader:

    def __init__(self, links):
        self.links = links
        self.results = []

    @staticmethod
    def get_session() -> Session:
        thread_local = local()
        if not hasattr(thread_local, 'session'):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_link(self, url: str):
        session = self.get_session()
        with session.get(url) as response:
            self.results.append(response.text)
            logger.info("Getting '%s'" % url)

    def download_all(self) -> None:
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.download_link, self.links)
