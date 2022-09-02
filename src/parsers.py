import abc
import sortedcontainers
from collections import Counter, namedtuple
from operator import methodcaller

import requests
from bs4 import BeautifulSoup
from loguru import logger


class BaseLinkParser(metaclass=abc.ABCMeta):
    """
    Parses all pages and gathers all links.
    """

    def __init__(self, start_url: str, tools: list):
        self.start_url = start_url
        self.tools = tools

    @abc.abstractmethod
    def get_all_links(self):
        """
        Returns list of all links for a single job offer.
        """
        ...

    @staticmethod
    def get_page(page_url: str):
        response = requests.get(page_url)
        return response.text

    @abc.abstractmethod
    def get_last_page_index(self):
        """
        Return amount of pages. If possible.
        """
        ...


class DjinniLinkParser(BaseLinkParser):

    def __init__(self, start_url, tools):
        self.all_data = ""
        self.start_page_data = requests.get(start_url).text
        self.offers_links = None
        self.BASE_URL = start_url
        super().__init__(start_url, tools)
        self.get_all_links()

    def get_base_url(self):
        return self.BASE_URL + "&page="

    def get_all_links(self):
        links = []
        for page_index in range(1, self.get_last_page_index() + 1):
            page_url = self.get_base_url() + str(page_index)
            logger.info("Getting '%s'" % page_url)
            page = self.get_page(page_url)
            parser = BeautifulSoup(page, "html.parser")
            links.extend(parser.findAll("a", class_="profile"))
        self.offers_links = links

    def get_last_page_index(self):
        # return 1
        html_parser = BeautifulSoup(self.start_page_data, "html.parser")
        try:
            # Black magic. Specific for djinni.
            last_tag = html_parser.findAll("a", class_="page-link")[-2]
        except IndexError:
            return 1
        return int(last_tag.text) + 1

    def get_data(self):
        all_data = []
        for item in self.offers_links:
            try:
                url = "https://djinni.co" + item["href"]
                logger.info("Getting '%s' (%s)" % (item.getText().strip(), url))
                parser = BeautifulSoup(self.get_page(url), "html.parser")
                profile = parser.find("p", class_="profile")
                data = parser.findAll("div", class_="profile-page-section")
                res = list(map(methodcaller("getText"), data))
                try:
                    profile_text = profile.getText()
                    all_data.append(profile_text)
                except AttributeError:
                    logger.error("Job has no profile section")
                t = ' '.join(res)
                all_data.append(t)
            except Exception as e:
                logger.critical(f"Failed to get page {e}")
        self.all_data = " ".join(all_data).replace("\n", ' ').lower()

    def handle_data(self):
        counter = Counter(self.all_data.lower().split())

        results = sortedcontainers.SortedList(key=lambda x: -x.results)
        SkillResult = namedtuple("Skill", "skill results")
        for tool in self.tools:
            amount = counter.get(tool) or 0
            results.add(
                SkillResult(tool, amount)
            )
        return results
