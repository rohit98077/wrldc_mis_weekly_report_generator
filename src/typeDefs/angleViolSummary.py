from typing import TypedDict, List
from src.typeDefs.angleViolation import IAngleViolation


class IAngleViolSummary(TypedDict):
    wideAnglViolations: List[IAngleViolation]
    adjAnglViolations: List[IAngleViolation]
