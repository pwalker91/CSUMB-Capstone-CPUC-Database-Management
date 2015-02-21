"""
------------------------------------------------------------------------
TCP_THREAD.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will represent a single thread, or pipe, in a network
            speed test. It will hold an array of Measurement objects, and has
            some basic object information

FUNCTIONS:
    __init__
------------------------------------------------------------------------
"""


# IMPORTS
from _Thread import Thread
#END IMPORTS

# CLASS
class TCP_Thread(Thread):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ThreadNumber    = 0
    # DataDirection   = ""
    # LocalIP         = ""
    # LocalPort       = 0000
    # ServerIP        = ""
    # ServerPort      = 0000
    # Measurements    = []
    # FinalMsmt       = None

    # Class attributes
    # ----------------------------------

    def __init__(self, dataArr=None, threadNum=0, direction="UP", units=("KBytes", "Kbits/sec")):
        """Call the parent class' __init__"""
        Thread.__init__(self, dataArr=dataArr, threadNum=threadNum, direction=direction, units=units)
    #END DEF
#END CLASS
