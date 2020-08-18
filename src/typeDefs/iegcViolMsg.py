from typing import TypedDict


class IIegcViolMsg(TypedDict):
    msgId: str
    date: str
    entity: str
    schedule: str
    drawal: str
    deviation: str
