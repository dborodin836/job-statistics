from flask import Flask, render_template

app = Flask(__name__)

SKILLS = [
    'python', 'js', 'sql', 'nosql', 'postgres', 'mysql', 'mongodb', 'aws', 'cloud',
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

LANGUAGES = [
    "dotnet", "android", "cplusplus", "flutter", "golang", "ios", "java", "javascript", "node.js",
    "php", "python", "ruby", "rust", "scala"
]


@app.route('/')
def home():
    return render_template("home.html", skills=SKILLS, languages=LANGUAGES)


if __name__ == '__main__':
    app.run(debug=True)
