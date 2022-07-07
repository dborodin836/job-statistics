from collections import Counter
from datetime import datetime
from operator import methodcaller

import requests
from bs4 import BeautifulSoup
from loguru import logger


BASE_URL = "https://djinni.co/jobs/keyword-python/?keywords=%28middle%7Cjunior%7Csenior%29" + "&page=1"


def get_last_page_index(data):
    parser = BeautifulSoup(data, "html.parser")
    try:
        last_tag = parser.findAll("a", class_="page-link")[-2]
    except IndexError:
        return 1
    return int(last_tag.text) + 1


def get_page(url):
    response = requests.get(url)
    data = response.text
    return data


def get_all_djinni_links():
    page = get_page(BASE_URL)
    links = []
    # for page_index in range(1, 2):
    for page_index in range(1, get_last_page_index(page) + 1):
        url = BASE_URL[:-1] + str(page_index)
        logger.info("Getting '%s'" % url)
        page = get_page(url)
        parser = BeautifulSoup(page, "html.parser")
        links.extend(parser.findAll("a", class_="profile"))
    return links


if __name__ == "__main__":
    djinni_links = get_all_djinni_links()
    all_data = []
    for item in djinni_links:
        try:
            url = "https://djinni.co" + item["href"]
            logger.info("Getting '%s' (%s)" % (item.getText().strip(), url))
            parser = BeautifulSoup(get_page(url), "html.parser")
            profile = parser.find("p", class_="profile")
            data = parser.findAll("div", class_="profile-page-section")
            res = map(methodcaller("getText"), data)
            try:
                profile_text = profile.getText()
            except AttributeError:
                logger.error("Job has no profile section")
            all_data.append(' '.join(res) + profile.getText())
            # print(all_data)
        except Exception:
            logger.critical("SHIT HAPPENS")
    data = " ".join(all_data).replace("\n", ' ').lower()

    counter = Counter(data.lower().split())

    with open(f"{str(datetime.now())[:10]}.txt", "w", encoding="utf-8") as file:
        file.write(data)


    def order_by_amount(x):
        try:
            res = int(x.split()[-1])
        except ValueError:
            return 0
        return res


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
