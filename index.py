import argparse
import datetime as dt
from docxtpl import DocxTemplate, InlineImage
from src.config.appConfig import getConfig
from src.utils.timeUtils import getWeekNumOfFinYr, getFinYearForDt
from src.fetchers.genUnitOutagesFetcher import fetchMajorGenUnitOutages
from src.fetchers.transElOutagesFetcher import fetchTransElOutages
from src.fetchers.longTimeUnrevivedForcedOutagesFetcher import fetchlongTimeUnrevivedForcedOutages
from src.fetchers.freqProfileFetcher import FrequencyProfileFetcher
from src.fetchers.vdiFetcher import VdiFetcher
from src.fetchers.voltStatsFetcher import VoltStatsFetcher
from src.fetchers.angleViolFetcher import AnglViolationsFetcher
from src.fetchers.iegcViolMsgsFetcher import IegcViolMsgsFetcher
from src.typeDefs.stationwiseVdiData import IStationwiseVdi
from src.typeDefs.outage import IOutage
from src.typeDefs.iegcViolMsg import IIegcViolMsg
from src.typeDefs.angleViolSummary import IAngleViolSummary
from src.typeDefs.appConfig import IAppConfig
from src.typeDefs.reportContext import IReportCxt
from typing import List

# get start and end dates from command line
# initialise default command line input values
startDate = dt.datetime.now() - dt.timedelta(days=1)
endDate = startDate - dt.timedelta(days=8)

# get an instance of argument parser from argparse module
parser = argparse.ArgumentParser()
# setup arguements
parser.add_argument('--start_date', help="Enter Start date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(startDate, '%Y-%m-%d'))
parser.add_argument('--end_date', help="Enter last date in yyyy-mm-dd format",
                    default=dt.datetime.strftime(endDate, '%Y-%m-%d'))
# get the dictionary of command line inputs entered by the user
args = parser.parse_args()

# access each command line input from the dictionary
startDate = dt.datetime.strptime(args.start_date, '%Y-%m-%d')
endDate = dt.datetime.strptime(args.end_date, '%Y-%m-%d')
endDate = endDate.replace(hour=23, minute=59, second=59)

startDateReportString = dt.datetime.strftime(startDate, '%d-%b-%Y')
endDateReportString = dt.datetime.strftime(endDate, '%d-%b-%Y')
weekNum = getWeekNumOfFinYr(startDate)
finYr = getFinYearForDt(startDate)
finYrStr = '{0}-{1}'.format(finYr, (finYr+1) % 100)

# get app db connection string from config file
appConfig: IAppConfig = getConfig()
appDbConStr: str = appConfig['appDbConStr']

# create context for weekly reoport
# initialise report context
reportContext: IReportCxt = {
    'startDt': startDateReportString,
    'endDt': endDateReportString,
    'wkNum': weekNum,
    'finYr': finYrStr,
    'genOtgs': [],
    'transOtgs': [],
    'longTimeOtgs': [],
    'freqProfRows': [],
    'weeklyFdi': -1,
    'wideViols': [],
    'adjViols': [],
    'voltStats': {
        'table1': [],
        'table2': [],
        'table3': [],
        'table4': []
    }
}

# get major generating unit outages
reportContext['genOtgs'] = fetchMajorGenUnitOutages(
    appDbConStr, startDate, endDate)

# get transmission element outages
reportContext['transOtgs'] = fetchTransElOutages(
    appDbConStr, startDate, endDate)

# get long time unrevived transmission element outages
reportContext['longTimeOtgs'] = fetchlongTimeUnrevivedForcedOutages(
    appDbConStr, startDate, endDate)

# get freq profile data
freqProfFetcher = FrequencyProfileFetcher(appDbConStr)
freqProfile = freqProfFetcher.fetchDerivedFrequency(startDate, endDate)
reportContext['freqProfRows'] = freqProfile['freqProfRows']
reportContext['weeklyFdi'] = round(freqProfile['weeklyFdi'], 3)

# get stationwise vdi data
vdiFetcher = VdiFetcher(appDbConStr)
vdiData: IStationwiseVdi = vdiFetcher.fetchWeeklyVDI(startDate)
reportContext['vdi400Rows'] = vdiData['vdi400Rows']
reportContext['vdi765Rows'] = vdiData['vdi765Rows']

# get stationwise voltage stats
voltStatsFetcher = VoltStatsFetcher(appDbConStr)
voltStats: dict = voltStatsFetcher.fetchDerivedVoltage(startDate, endDate)
reportContext['voltStats'] = voltStats

# get iegc violation messages
violMsgsFetcher = IegcViolMsgsFetcher(appDbConStr)
violMsgs: List[IIegcViolMsg] = violMsgsFetcher.fetchIegcViolMsgs(
    startDate, endDate)
reportContext['violMsgs'] = violMsgs

# get pairs angle violations
anglViolsFetcher = AnglViolationsFetcher(appDbConStr)
pairAnglViolations: IAngleViolSummary = anglViolsFetcher.fetchPairsAnglViolations(
    startDate, endDate)
reportContext['wideViols'] = pairAnglViolations['wideAnglViols']
reportContext['adjViols'] = pairAnglViolations['adjAnglViols']

# generate report word file
tmplPath = "assets/weekly_report_template.docx"
doc = DocxTemplate(tmplPath)

# # signature Image
# signatureImgPath = 'assets/signature.png'
# signImg = InlineImage(doc, signatureImgPath)
# reportContext['signature'] = signImg

doc.render(reportContext)
doc.save("dumps/weekly_report.docx")
print('Weekly report generation done...')
