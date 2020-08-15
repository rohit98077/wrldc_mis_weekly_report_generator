import pandas as pd
from typing import TypedDict


class AppConfig(TypedDict):
    appDbConStr: str


def getConfig(configFilename='config.xlsx') -> AppConfig:
    """[summary]
    Get the application config from config.xlsx file
    Returns:
        dict: The application configuration as a dictionary
    """

    df = pd.read_excel(configFilename, header=None, index_col=0)
    configDict = df[1].to_dict()
    return configDict
