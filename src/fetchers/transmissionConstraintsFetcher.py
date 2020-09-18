import cx_Oracle
import pandas as pd
import datetime as dt
from typing import List, Tuple
from src.typeDefs.transConstraint import ITransConstraint


class TransConstraintsFetcher():
    """This class fetches Transmission Constraints for weekly report
    """

    def __init__(self, con_string: str):
        """constructor method
        Args:
            con_string ([str]): connection string
        """

        self.connString = con_string

    def fetchTransConstraints(self, startDate: dt.datetime, endDate: dt.datetime) -> List[ITransConstraint]:
        """fetch Transmission Constraints for weekly report from warehouse db 
        Args:
            startDate (dt.datetime): start date
            endDate (dt.datetime): end date
        Returns:
            List[ITransConstraint]: List of Transmission Constraints for weekly report
        """

        try:
            connection = cx_Oracle.connect(self.connString)
            cursor = connection.cursor()

            sql_fetch = """
                        select * from transmission_constraint_data
                        where 
                        start_date IN 
                        (select max(start_date) from transmission_constraint_data)
                        """
            cursor.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD' ")
            df = pd.read_sql(sql_fetch, con=connection)
        except:
            print('Error while fetching data from db')
        finally:
            # closing database cursor and connection
            if cursor is not None:
                cursor.close()
            connection.close()
            print('closed db connection after transmission constraints fetching')

        transConstraints: List[ITransConstraint] = []
        for i in df.index:
            transCons: ITransConstraint = {
                'corridor': df['CORRIDOR'][i],
                'season': df['SEASON_ANTECEDENT'][i],
                'description': df['DESCRIPTION_CONSTRAINTS'][i]
            }
            transConstraints.append(transCons)
        return transConstraints
