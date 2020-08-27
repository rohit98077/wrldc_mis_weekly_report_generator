from typing import TypedDict, List
from src.typeDefs.outage import IOutage
from src.typeDefs.dayFreqProfile import IDayFreqProfile
from src.typeDefs.stationVdiProfile import IStationVdiProfile
from src.typeDefs.iegcViolMsg import IIegcViolMsg


class VoltageStatsDict(TypedDict):
    table1: List[dict]
    table2: List[dict]
    table3: List[dict]
    table4: List[dict]


class IReportCxt(TypedDict):
    startDt: str
    endDt: str
    wkNum: float
    finYr: str
    genOtgs: List[IOutage]
    transOtgs: List[IOutage]
    longTimeOtgs: List[IOutage]
    freqProfRows: List[IDayFreqProfile]
    weeklyFdi: float
    vdi400Rows: List[IStationVdiProfile]
    vdi765Rows: List[IStationVdiProfile]
    violMsgs: List[IIegcViolMsg]
    voltStats: VoltageStatsDict
