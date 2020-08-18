from typing import TypedDict, List
from src.typeDefs.outage import IOutage
from src.typeDefs.dayFreqProfile import IDayFreqProfile
from src.typeDefs.stationVdiProfile import IStationVdiProfile
from src.typeDefs.iegcViolMsg import IIegcViolMsg


class IReportCxt(TypedDict):
    genOtgs: List[IOutage]
    transOtgs: List[IOutage]
    longTimeOtgs: List[IOutage]
    freqProfRows: List[IDayFreqProfile]
    weeklyFdi: float
    vdi400Rows: List[IStationVdiProfile]
    vdi765Rows: List[IStationVdiProfile]
    violMsgs: List[IIegcViolMsg]
