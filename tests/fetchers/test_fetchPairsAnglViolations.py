import unittest
import datetime as dt
from src.config.appConfig import getConfig
from src.fetchers.angleViolFetcher import AnglViolationsFetcher
from src.typeDefs.angleViolSummary import IAngleViolSummary
from typing import List


class TestAnglViolationsFetch(unittest.TestCase):
    appDbConStr: str = ''

    def setUp(self):
        appConfig = getConfig()
        self.appDbConStr = appConfig['appDbConStr']

    def test_run(self) -> None:
        """tests the function that fetches the ouatges from reporting software
        """
        startDate = dt.datetime(2020, 8, 9)
        endDate = dt.datetime(2020, 8, 15)

        anglViolFetcher = AnglViolationsFetcher(self.appDbConStr)
        violData: IAngleViolSummary = anglViolFetcher.fetchPairsAnglViolations(
            startDate, endDate)
        # print(outages)
        self.assertTrue(len(violData['wideAnglViols']) > 0)
        self.assertTrue(len(violData['adjAnglViols']) > 0)
