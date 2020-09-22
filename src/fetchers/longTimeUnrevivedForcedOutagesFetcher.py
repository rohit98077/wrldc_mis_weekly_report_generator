import datetime as dt
import cx_Oracle
from typing import List
from src.typeDefs.outage import IOutage


def fetchlongTimeUnrevivedForcedOutages(conStr: str, startDt: dt.datetime, endDt: dt.datetime) -> List[IOutage]:
    """fetch forced outages that are still out and outage duration greater than 6 months
    here we take (revived time = null) or (revived time > endTimeInput)

    Args:
        conStr (str): connection string to reports database
        startDt (dt.datetime): start date of report time scope
        endDt (dt.datetime): end date of report time scope

    Returns:
        List[IOutage]: list of outage objects that contain the following data
        element_name, owners, capacity, outage date, outage time, revival date, revival time, reason
    """
    # connect to app database
    con = cx_Oracle.connect(conStr)

    # sql query to fetch the outages
    outagesFetchSql = '''SELECT oe.ELEMENT_NAME, 
    oe.OWNERS, oe.CAPACITY,
    oe.OUTAGE_DATETIME, oe.REVIVED_DATETIME,
    oe.OUTAGE_REMARKS, oe.REASON, oe.shutdown_tag
    from mis_warehouse.outage_events oe 
    where (oe.shutdown_typename = 'FORCED') and 
    (oe.OUTAGE_DATETIME < :1) and
    ((oe.REVIVED_DATETIME IS NULL) or (oe.REVIVED_DATETIME>:1)) and
    ((:1 - oe.OUTAGE_DATETIME) > INTERVAL '180' DAY(3)) 
    order by oe.OUTAGE_DATETIME
    '''

    # get cursor and execute fetch sql
    cur = con.cursor()
    cur.execute(outagesFetchSql, (endDt,))
    colNames = [row[0] for row in cur.description]
    targetColumns = ['ELEMENT_NAME', 'OWNERS', 'CAPACITY',
                     'OUTAGE_DATETIME', 'REVIVED_DATETIME', 'OUTAGE_REMARKS', 'REASON', 'SHUTDOWN_TAG']
    if (False in [(col in targetColumns) for col in colNames]):
        # all desired columns not fetched, hence return empty
        return []
    # print(colNames)

    # fetch all rows
    dbRows = cur.fetchall()

    # initialise outages to be returned
    outages: List[IOutage] = []

    elNameInd = colNames.index('ELEMENT_NAME')
    ownersInd = colNames.index('OWNERS')
    capInd = colNames.index('CAPACITY')
    outDtInd = colNames.index('OUTAGE_DATETIME')
    reviveDtInd = colNames.index('REVIVED_DATETIME')
    remarksInd = colNames.index('OUTAGE_REMARKS')
    reasonInd = colNames.index('REASON')
    outageTagInd = colNames.index('SHUTDOWN_TAG')

    # iterate through each row to populate result outage rows
    for row in dbRows:
        elName: str = row[elNameInd]
        owners: str = row[ownersInd]
        voltLvl: str = str(row[capInd])
        outDateStr: str = dt.datetime.strftime(row[outDtInd], "%d-%m-%Y")
        outTimeStr: str = dt.datetime.strftime(row[outDtInd], "%H:%M")
        revivalDateStr: str = 'Still out'
        revivalTimeStr: str = 'Still out'
        revivalDt = row[reviveDtInd]
        if not(revivalDt == None):
            revivalDateStr = dt.datetime.strftime(revivalDt, "%d-%m-%Y")
            revivalTimeStr = dt.datetime.strftime(revivalDt, "%H:%M")
        reason = row[reasonInd]
        remarks = row[remarksInd]
        outageTag = row[outageTagInd]
        if outageTag == 'Outage':
            outageTag = None
        reasonStr = ' / '.join([r for r in [outageTag, reason,
                                            remarks] if not(r == None)])
        # create outage record
        outageObj: IOutage = {
            'elName': elName,
            'owners': owners,
            'capacity': voltLvl,
            'outageDate': outDateStr,
            'outageTime': outTimeStr,
            'revivalDate': revivalDateStr,
            'revivalTime': revivalTimeStr,
            'reason': reasonStr
        }
        outages.append(outageObj)
    return outages
