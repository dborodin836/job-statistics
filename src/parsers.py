import abc
from collections import Counter
from datetime import datetime
from operator import methodcaller

import requests
from bs4 import BeautifulSoup
from loguru import logger


class BaseLinkParser(metaclass=abc.ABCMeta):
    """
    Parses all pages and gathers all links.
    """

    def __init__(self, start_url: str):
        self.start_url = start_url

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

    def __init__(self, start_url):
        self.start_page_data = requests.get(start_url).text
        self.offers_links = None
        self.BASE_URL = start_url
        super().__init__(start_url)
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
                res = map(methodcaller("getText"), data)
                try:
                    profile_text = profile.getText()
                except AttributeError:
                    logger.error("Job has no profile section")
                all_data.append(' '.join(res) + profile.getText())
            except Exception:
                logger.critical("Failed to get page")
        return " ".join(all_data).replace("\n", ' ').lower()


def print_djinni_data():
    data = DjinniLinkParser(
        "https://djinni.co/jobs/keyword-python/?keywords=%28middle%7Cjunior").get_data()

    counter = Counter(data.lower().split())

    with open(f"{str(datetime.now())[:10]}.txt", "w", encoding="utf-8") as file:
        file.write(data)

    def order_by_amount(x):
        try:
            return int(x.split()[-1])
        except ValueError:
            return 0

    # tools =
    tools = ['python', 'js', 'sql', 'nosql', 'postgres', 'mysql', 'mongodb', 'aws', 'cloud',
             'fastapi', 'django', 'flask', 'celery', 'redis', 'docker', 'docker swarm', 'asyncio',
             'git', 'gcp', 'azure', 'react', 'angular', 'kubernetes', 'sqlalchemy', 'keydb',
             'memcached', 'jenkins', 'kafka', 'helm', 'rabbitmq', 'typescript', 'terraform',
             'kibana', 'sentry', 'logrocket', 'pagerduty', 'prometheus', 'grafana', 'djangorest',
             'javascript', 'postgresql', 'rest', 'restful', 'solid', "aiohtpp", "patterns", "oop",
             "linux", "graphql", "ci/cd", "agile", "ajax", "unix", "pytest", "unittest", "css",
             "css3", "html5", "html", "react.js", "jira", "selenium", "reactjs", "vue", "orm",
             "jquery", "openapi", "github", "gitlab", "scrapy", "drf", "pyramid", "http",
             "puppeteer", "rdbms", "apollo", "elasticsearch", "python3", "spa", "istio", "tdd",
             "kiss", "dry", "docker-compose", "docker compose", "microservice", "microservices",
             "websockets", "go", "golang", "java", "php", "k8s", "elastic", "redpanda", "soap",
             ]

    results = []
    for tool in tools:
        results.append(f"{tool} | {counter.get(tool)}".rjust(20))
    results.sort(key=order_by_amount, reverse=True)
    print(*results, sep="\n")
    return '\n'.join(results)
