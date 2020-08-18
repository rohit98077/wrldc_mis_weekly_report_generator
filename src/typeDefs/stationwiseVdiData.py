from typing import TypedDict, List
from src.typeDefs.stationVdiProfile import IStationVdiProfile


class IStationwiseVdi(TypedDict):
    vdi400Rows: List[IStationVdiProfile]
    vdi765Rows: List[IStationVdiProfile]
