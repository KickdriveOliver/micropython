"""mccom module stub/interface for fullmo MovingCap servo drives

The mccom Python module/library provides communication channels for network communication with MovingCap, but 
also extending standard MovingCap protocols like RefGo.

This is currently a first implementation that only supports "refgo" applications, see below. 
"""
__author__ =  "Oliver Heggelbacher"
__email__ = "oliver.heggelbacher@fullmo.de"
__version__ = "50.00.08.xx"
__date__ = "2025-02-03"

def open(channelSetting : str, index: int) -> int:
    """Opens a new communication channel, e.g access the standard "RefGo" port 10001

    :param channelSetting: specifies the type of socket or communication channel to use. 
        Default is "refgo" - read and write to the RefGo protocol TCP port 10001.
    :type channelSetting: str
    :param index: A integer index to reference this channel when using the other Comm... commands. 
        default is zero. 
    :type index: int
    :return: 1 if error. 0 if no error.
    :rtype: int
    """

def read(index: int, readType: int) -> str: 
    """Reads all data available (or parts of it) for the specified index

    :param index: the comm index as specified when calling CommOpen
    :type index: int
    :param readType: read access type: currently only
        0 - read next ASCII line (default), 
    :type readType: int
    :return: the data as string, Empty string if no data available.
    :rtype: str
    """

def write(index: int, writeType: int, msg: str) -> int: 
    """Writes the data from str to the specified communication index

    :param index: the comm index as specified when calling CommOpen
    :type index: int
    :param writeType: write access type: currently only
        0 - write as text, add line end (CR/LF) as needed
    :type writeType: int
    :param msg: the actual data to write
    :type msg: str   
    :return: 1 if error. 0 if no error.
    :rtype: int
    """

def close(index: int):
    """Closes a communication channel

    :param index: the comm index as specified when calling CommOpen
    :type index: int
    """