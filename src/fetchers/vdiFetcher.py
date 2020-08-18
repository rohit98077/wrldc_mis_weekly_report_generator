import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.stationwiseVdiData import IStationwiseVdi
from src.typeDefs.stationVdiProfile import IStationVdiProfile
from src.utils.stringUtils import convertHrsToSpanStr


class VdiFetcher():
    """fetches VDI data for populating weekly mis report
    """

    def __init__(self, appDbConnStr: str):
        """constructor method
        Args:
            con_string ([type]): connection string of application db that contains VDI derived data
        """

        self.connString = appDbConnStr

    def toDerivedVDIDict(self, df: pd.core.frame.DataFrame) -> IStationwiseVdi:
        """returns derivedVDIDict that has two keys 
        derivedVDIDict['VDIRows400'] = VDIRows400Kv
        derivedVDIDict['VDIRows765'] = VDIRows765Kv
        Args:
            df (pd.core.frame.DataFrame): pandas dataframe
        Returns:
            IStationwiseVdi: week VDI summary data for each 765 and 400 kv station 
        """

        del[df['ID'], df['MAPPING_ID'], df['WEEK_START_DATE']]
        VDIRows400Kv: List[IStationVdiProfile] = []
        VDIRows765Kv: List[IStationVdiProfile] = []
        derivedVDIDict: IStationwiseVdi = {
            'vdi400Rows': [],
            'vdi765Rows': []
        }

        group = df.groupby("NODE_VOLTAGE")
        for nameOfGroup, groupDf in group:
            if nameOfGroup == 400:
                for ind in groupDf.index:
                    tempDict = {
                        'station': groupDf['NODE_NAME'][ind],
                        'maxVol': groupDf['MAXIMUM'][ind],
                        'minVol': groupDf['MINIMUM'][ind],
                        'lessThanBand': round(groupDf['LESS_THAN_BAND'][ind], 2),
                        'bwBand': round(groupDf['BETWEEN_BAND'][ind], 2),
                        'greatThanBand': round(groupDf['GREATER_THAN_BAND'][ind], 2),
                        'lessBandHrs': convertHrsToSpanStr(groupDf['LESS_THAN_BAND_INHRS'][ind]),
                        'greatBandHrs': convertHrsToSpanStr(groupDf['GREATER_THAN_BAND_INHRS'][ind]),
                        'outOfBandHrs': convertHrsToSpanStr(groupDf['OUT_OF_BAND_INHRS'][ind]),
                        'vdi': round(groupDf['VDI'][ind], 2)
                    }
                    VDIRows400Kv.append(tempDict)
            elif nameOfGroup == 765:
                for ind in groupDf.index:
                    tempDict = {
                        'station': groupDf['NODE_NAME'][ind],
                        'maxVol': groupDf['MAXIMUM'][ind],
                        'minVol': groupDf['MINIMUM'][ind],
                        'lessThanBand': round(groupDf['LESS_THAN_BAND'][ind], 2),
                        'bwBand': round(groupDf['BETWEEN_BAND'][ind], 2),
                        'greatThanBand': round(groupDf['GREATER_THAN_BAND'][ind], 2),
                        'lessBandHrs': convertHrsToSpanStr(groupDf['LESS_THAN_BAND_INHRS'][ind]),
                        'greatBandHrs': convertHrsToSpanStr(groupDf['GREATER_THAN_BAND_INHRS'][ind]),
                        'outOfBandHrs': convertHrsToSpanStr(groupDf['OUT_OF_BAND_INHRS'][ind]),
                        'vdi': round(groupDf['VDI'][ind], 2)
                    }
                    VDIRows765Kv.append(tempDict)
        derivedVDIDict['vdi400Rows'] = VDIRows400Kv
        derivedVDIDict['vdi765Rows'] = VDIRows765Kv
        return derivedVDIDict

    def fetchWeeklyVDI(self, startDate: dt.datetime) -> IStationwiseVdi:
        """fetched derived VDI from mis_warehouse db
        Args:
            startDate (dt.datetime): start-date
        Returns:
            IStationwiseVdi: week VDI summary data for each 765 and 400 kv station 
        """

        try:
            connection = cx_Oracle.connect(self.connString)

        except Exception as err:
            print('error while creating a connection', err)

        else:
            # print(connection.version)
            try:
                cur = connection.cursor()
                fetch_sql = '''select vdi.* from 
                            mis_warehouse.derived_vdi vdi, mis_warehouse.voltage_mapping_table mt
                            where vdi.mapping_id = mt.id and mt.is_included_in_weekly = 'T' and week_start_date = to_date(:start_date)'''

                cur.execute(
                    "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
                df = pd.read_sql(fetch_sql, params={
                                 'start_date': startDate}, con=connection)

            except Exception as err:
                print('error while fetching weekly VDI data', err)
            else:
                print('VDI data fetch complete')
                connection.commit()
        finally:
            cur.close()
            connection.close()
            print("connection closed")

        derivedVDIDict = self.toDerivedVDIDict(df)
        return derivedVDIDict
