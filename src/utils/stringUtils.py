def addTrailingZeroForTimeComp(nVal: int) -> str:
    """add trailing zero to number <10

    Args:
        nVal (int): input number

    Returns:
        str: output string
    """
    if nVal < 10 and nVal >= 0:
        return '0{0}'.format(nVal)
    else:
        return '{0}'.format(nVal)


def convertHrsToSpanStr(nHrs) -> str:
    """convert number of hours to string, like 29.6 to 29:36

    Args:
        nHrs ([type]): [description]

    Returns:
        str: [description]
    """
    hrs = addTrailingZeroForTimeComp(int(nHrs // 1))
    mins = addTrailingZeroForTimeComp(int(round((nHrs % 1)*60)))
    spanStr = '{0}:{1}'.format(hrs, mins)
    return spanStr
