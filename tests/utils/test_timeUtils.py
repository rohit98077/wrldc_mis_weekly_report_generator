import unittest
import datetime as dt
from src.utils.timeUtils import getWeekNumOfFinYr, getFinYearForDt


class TestTimeUtils(unittest.TestCase):
    def test_weekNum(self) -> None:
        """tests the function that get the week number for a given input date
        """
        inpDt = dt.datetime(2020, 8, 10)
        weekNum = getWeekNumOfFinYr(inpDt)
        self.assertTrue(weekNum == 20)

    def test_finYr(self) -> None:
        """tests the function that get the financial year of input time
        """
        inpDt = dt.datetime(2020, 3, 31)
        finYr = getFinYearForDt(inpDt)
        self.assertTrue(finYr == 2020)
