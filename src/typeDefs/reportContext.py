from typing import TypedDict, List
from src.typeDefs.outage import IOutage
from src.typeDefs.dayFreqProfile import IDayFreqProfile


class IReportCxt(TypedDict):
    genOtgs: List[IOutage]
    transOtgs: List[IOutage]
    longTimeOtgs: List[IOutage]
    freqProfRows: List[IDayFreqProfile]
    weeklyFdi: float