"""
------------------------------------------------------------------------
__BASE.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a few classes that have qualities common between all of the
            classes in this project. This includes things like error status,
            error code, string formatting, etc.
CLASSES:
    Formatting
    ErrorHandling
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit





"""
------------------------------------------------------------------------
FORMATTING Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Provides a base class for inheritting variables that pertain
            to formatting of file output
-----------------------------------------------------------------------
"""


class Formatting(object):

    """A Class for common string formatting across objects"""

    def __init__(self):
        """Object initialization"""
        self.StringPadding = "    "
        self.ConfirmedCarriers = ["AT&T", "Verizon", "Sprint", "T-Mobile"]
    #END DEF
#END CLASS




"""
------------------------------------------------------------------------
FORMATTING Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Provides a base class for inheritting variables that pertain
            to formatting of file output
-----------------------------------------------------------------------
"""


class ErrorHandling(object):

    """A simple class containing error types and codes"""

    #Some Static class variables
    __ErrorTypes = {
            101: "Output Error",
            102: "Write Failure",
            103: "Bad Exit Value",
            111: "Ping Timeout",
            112: "Network Unreachable",
            121: "Test Timeout",
            131: "No ACK Received",
            201: "Quit by User",
            202: "Wrong Connection Made",
            210: "Test Not Performed",
            310: "No Tests Performed",
            311: "Connectivity Test Failed",
            404: "Unknown Error"
    }
    __ErrorMessages = {
            101: "There was an error in the output of the data.",
            102: "There was a failure in the output pipe, and data could not be written.",
            103: "There was an error of some kind. The test was quit with a bad exit value",
            111: "The ping timed out.",
            112: "The network was unreachable for this test.",
            121: "The test timed out.",
            131: "An ACK of last datagram was not received after multiple tries.",
            201: "The test was quite prematurely by the user.",
            202: "The test performed was connected to the wrong server.",
            210: "The test did not complete, or was not performed.",
            310: "No tests were performed and recorded in this file.",
            311: "Could not connect to a server. Tests were not started",
            404: "Unknown Error"
    }

    def __init__(self):
        """Object initialization"""
        self.ContainsErrors = False
        self.ErrorCode = 0
        self.ErrorType = ""
        self.ErrorMessage = ""
    #END DEF

    def __setErrorCode(self, code, *args):
        """Sets this objects Error Code to the given code, and ContainsErrors to True"""
        if code not in self.__ErrorTypes.keys():
            raise ValueError("Error code must be one of these types.\n"+
                             "{}".format(self.ErrorTypes.keys()))
        self.ErrorCode = code
        self.ContainsErrors = True
        self.ErrorType = self.__ErrorTypes[code]
        if len(args) == 1:
            self.ErrorMessage = args[0]
        else:
            self.ErrorMessage = self.__ErrorMessages[code]
        return True
    #END DEF
#END CLASS
