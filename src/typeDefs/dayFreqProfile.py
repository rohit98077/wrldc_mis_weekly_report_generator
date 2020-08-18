from typing import TypedDict


class IDayFreqProfile(TypedDict):
    date_day: float
    max_freq: float
    min_freq: float
    avg_freq: float
    less_than_band: float
    bw_band: float
    great_than_band: float
    out_of_band: float
    out_hrs: float
    fdi: float