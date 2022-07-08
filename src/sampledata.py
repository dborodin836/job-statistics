from dataclass import Job
from enums import Skill as s, Position as p

data = [
    Job("https://djinni.co/jobs/413135-middle-python-backend-developer/",
        skills=[s.python, s.postgres, s.mysql, s.aws, s.cloud, s.fastapi, s.selenium, s.django,
                s.flask, s.scrappy, s.celery, s.redis, s.rabbitmq, s.docker, s.asyncio,
                s.docker_swarm],
        position=p.middle
        ),
    Job("https://djinni.co/jobs/413135-middle-python-backend-developer/",
        skills=[s.python, s.aws, s.django, s.flask, s.git, s.azure, s.sql],
        position=p.middle
        ),
    Job("https://djinni.co/jobs/439201-python-fullstack-developer/",
        skills=[s.python, s.aws, s.flask, s.celery, s.redis, s.docker, s.sql, s.js, s.nosql,
                s.kubernetes, s.sqlalchemy, s.keydb, s.memcached, s.jenkins, s.kafka, s.helm],
        position=p.middle
        ),
    Job("https://djinni.co/jobs/409749-middle-backend-engineer-python-for-a-business/",
        skills=[s.aws, s.python, s.django, s.postgres, s.js, s.react, s.typescript, s.jenkins,
                s.docker, s.kubernetes, s.terraform, s.kibana, s.sentry, s.logrocket, s.pagerduty,
                s.prometheus, s.grafana],
        position=p.middle
        ),
    Job("https://djinni.co/jobs/440751-middle-backend-python-developer/",
        skills=[s.python, s.django, s.djangorest, s.flask, s.fastapi, s.aws, s.sql, s.nosql,
                s.docker, s.kubernetes],
        position=p.middle
        ),

]
