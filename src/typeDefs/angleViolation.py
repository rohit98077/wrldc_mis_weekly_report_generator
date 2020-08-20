from typing import TypedDict


class IAngleViolation(TypedDict):
    pairName: str
    angularLim: float
    violPerc: str
    maxDeg: str
    minDeg: str