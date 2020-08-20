from typing import TypedDict, List
from src.typeDefs.angleViolation import IAngleViolation


class IAngleViolSummary(TypedDict):
    wideAnglViols: List[IAngleViolation]
    adjAnglViols: List[IAngleViolation]
