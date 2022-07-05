import dataclasses
from enums import Position


@dataclasses.dataclass
class Job:
    link: str
    skills: list
    position: Position


class BaseJob:
    link: str
    title: str
    data: str
    position: Position

