"""
------------------------------------------------------------------------
TCP_THREAD.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE-  This object will represent a single thread, or pipe, in a network
            speed test. It will hold an array of Measurement objects, and has
            some basic object information

VARIABLES:
  INHERITED
    ThreadNumber          Integer, the number thread this is (is between 3 and 6
    DataDirection       String, is either Up or Down (depending on the order of the thread's read
    LocalIP             The IP of this test's local machine
    LocalPort           The port of this test's local machine
    ServerIP            The IP of the server this thread was connected to
    ServerPort          The port of the server this thread was connected to
    Measurements      List, holding all of the Pings in this specific thread
    FinalMsmt         Ping object, holding the final summation ping in the list

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
                    dataArr:    List of Strings, each String is a measurement that will be parsed and stored
                                in this object
                    ThreadNum:  Integer, the number that this thread is (generally between 3 and 6)
                    direction:  String, the direction of the data in this thread (UP or DOWN)
                    units:      Tuple of two Strings, the units being used by the measurements
                    short:      Boolean, determines detail of printout in __str__
        OUTPUTS-    none
------------------------------------------------------------------------
"""


# IMPORTS
from PyObjects._Thread import Thread
#END IMPORTS

# CLASS
class TCP_Thread(Thread):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # ThreadNumber    = 0
    # DataDirection   = ""
    # LocalIP         = ""
    # LocalPort       = 0
    # ServerIP        = ""
    # ServerPort      = 0
    # Measurements    = []
    # FinalMsmt       = None

    # Class attributes
    # ----------------------------------

    # DESC: Initializing class
    def __init__(self, dataArr=None, threadNum=0, direction="UP", units=("KBytes", "Kbits/sec")):
        #Call the parent class' __init__
        Thread.__init__(self, dataArr=dataArr, threadNum=threadNum, direction=direction, units=units)
    #END DEF
#END CLASS
