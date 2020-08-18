import datetime as dt
from src.fetchers.genUnitOutagesFetcher import fetchMajorGenUnitOutages
from src.fetchers.transElOutagesFetcher import fetchTransElOutages
from src.fetchers.longTimeUnrevivedForcedOutagesFetcher import fetchlongTimeUnrevivedForcedOutages


def getWeeklyReportContextObj(appDbConStr: str, startDt: dt.datetime, endDt: dt.datetime) -> dict:
    contextObj: dict = {}
    contextObj['majorGenOutages'] = fetchMajorGenUnitOutages(
        appDbConStr, startDt, endDt)
    contextObj['transOutages'] = fetchTransElOutages(
        appDbConStr, startDt, endDt)
    contextObj['longOutages'] = fetchlongTimeUnrevivedForcedOutages(
        appDbConStr, startDt, endDt)
    return contextObj
