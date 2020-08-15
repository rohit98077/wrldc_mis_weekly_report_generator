import unittest
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.genUnitOutagesFetcher import fetchMajorGenUnitOutages, Outage
from typing import List


class TestFetchGenUnitOutages(unittest.TestCase):
    appDbConStr: str = ''

    def setUp(self):
        appConfig = getConfig()
        self.appDbConStr = appConfig['appDbConStr']

    def test_run(self) -> None:
        """tests the function that fetches the ouatges from reporting software
        """
        startDate = dt.datetime(2019, 10, 10)
        endDate = dt.datetime(2019, 10, 25)

        outages: List[Outage] = fetchMajorGenUnitOutages(
            self.appDbConStr, startDate, endDate)
        # print(outages)
        self.assertTrue(len(outages) > 0)
