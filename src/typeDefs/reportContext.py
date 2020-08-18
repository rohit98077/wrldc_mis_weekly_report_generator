from typing import TypedDict, List
from src.typeDefs.outage import IOutage


class IReportCxt(TypedDict):
    genOtgs: List[IOutage]
    transOtgs: List[IOutage]
    longTimeOtgs: List[IOutage]