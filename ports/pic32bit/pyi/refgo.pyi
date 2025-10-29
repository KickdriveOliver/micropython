"""refgo module stub/interface for fullmo MovingCap servo drives

The refgo Python module/library provides access to the ASCII protocol interpreter on TCP port 10001
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.08.xx"
__date__ = "2025-02-03"

def cmd(command: str) -> str:
    """Executes RefGo command and returns answer 

    :param command: the RefGo command string, without CR / end of line. E.g. 'TS'
    :type command: str
    :return: answer string for the command. For TS and TP the return value type is int for increased performance.
    :rtype: str or int
    """