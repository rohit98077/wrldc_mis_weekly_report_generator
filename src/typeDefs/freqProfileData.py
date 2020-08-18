from typing import TypedDict, List
from src.typeDefs.dayFreqProfile import IDayFreqProfile


class IFreqProfile(TypedDict):
    freqProfRows: List[IDayFreqProfile]
    weeklyFdi: float
