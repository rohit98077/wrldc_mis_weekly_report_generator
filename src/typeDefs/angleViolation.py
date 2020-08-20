from typing import TypedDict


class IAngleViolation(TypedDict):
    pairName: str
    angularLim: float
    violation: str
    maxDeg: str
    minDeg: str