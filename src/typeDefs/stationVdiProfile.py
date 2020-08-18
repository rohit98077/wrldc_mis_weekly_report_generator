from typing import TypedDict


class IStationVdiProfile(TypedDict):
    station: str
    maxVol: float
    minVol: float
    lessThanBand: float
    bwBand: float
    greatThanBand: float
    lessBandHrs: str
    greatBandHrs: str
    outOfBandHrs: str
    vdi: float
