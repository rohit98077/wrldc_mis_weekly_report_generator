from typing import TypedDict


class IAngleViolation(TypedDict):
    pairName: str
    angularLim: float
    violPerc: float
    maxDeg: float
    minDeg: float