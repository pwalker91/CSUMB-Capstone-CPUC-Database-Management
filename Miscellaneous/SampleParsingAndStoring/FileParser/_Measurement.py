#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
_MEASUREMENT.PY

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single measurement of data transfer speed in a single test
            (i.e. This object represent one line of text in a speed test)
            This file include the base Measurement class, as well as the slightly
            modified Final_Measurement class, and the more specialized
            UDP_ServerReport class.
CLASSES:
    Measurement
    Final_Measurement
    UDP_ServerReport
------------------------------------------------------------------------
"""
if __name__=="__main__":
    raise SystemExit

# IMPORTS
from __Base import Formatting
#END IMPORTS




"""
------------------------------------------------------------------------
MEASUREMENT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single measurement of data transfer speed in a single test
            (i.e. This object represent one line of text in a speed test)
-----------------------------------------------------------------------
"""


class Measurement(Formatting):

    """A generic Measurement object. Hold the start time, end time, speed, and size"""

    '''
    # ------------------------------
    # ---- CLASS ATTRIBUTES ----
    TimeStart       = 0.0
    TimeEnd         = 0.0
    Size            = 0.0
    size_units      = ""
    Speed           = 0.0
    speed_units     = ""
    # ------------------------------
    '''

    def __init__(self, data, units=("KBytes","Kbits/sec")):
        """
        Used to initialize an object of this class
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
            data:   String, the measurement that will be parsed for data
            units:  Tuple of two Strings, the units being used by the measurement
        """
        #Setting up the whitespace padding that this class will need to use
        Formatting.__init__(self)
        self.StringPadding = self.StringPadding*4
        #First, assigning the size and speed units to the necessary class variables
        self.size_units, self.speed_units = units

        #This takes the given data String and parses the object information
        #First, split the string on the "-" between the time measurements
        data_start  = data.split("-")[0].split("]")[1].strip()
        data        = data.split("-")[1]
        #Then, split on the first instance of "sec", which should follow the second time measurement
        data_end    = data.split("sec",1)[0].strip()
        data        = data.split("sec",1)[1]
        #Next, split the remaining string along the size units
        data_size   = data.split(self.size_units)[0].strip()
        data        = data.split(self.size_units)[1]
        #Now, we only have to split was is left on the speed units
        data_speed  = data.split(self.speed_units)[0].strip()

        #Now, we cast all of those parsed measurements as floats
        self.TimeStart  = float(data_start)
        self.TimeEnd    = float(data_end)
        self.Size       = float(data_size)
        self.Speed      = float(data_speed)
    #END DEF

    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding +
                #ljust() and rjust() are justification functions. This is so that
                # all of the text lines up nicely
                ("{}".format(self.TimeStart).rjust(4)+"-"+
                 "{}".format(self.TimeEnd).rjust(4)+" sec").ljust(15) +
                "{:.2f} {}".format(self.Size,self.size_units).rjust(16) +
                "{:.2f} {}".format(self.Speed,self.speed_units).rjust(22)
                )
    #END DEF
#END CLASS





"""
------------------------------------------------------------------------
FINAL_MEASUREMENT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single measurement of data transfer speed in a single test
            (i.e. This object represent one line of text in a speed test)
-----------------------------------------------------------------------
"""


class Final_Measurement(Measurement):

    """The same as a Measurment class, only with a modified __str__ statment"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    TimeStart       = 0.0
    TimeEnd         = 0.0

    Size            = 0.0
    size_string     = ""
    size_units      = ""
    #_size_pad = ""

    Speed           = 0.0
    speed_string    = ""
    speed_units     = ""
    #_speed_pad = ""
    '''

    def __init__(self, data, units=("KBytes","Kbits/sec")):
        """Call parent's __init__"""
        Measurement.__init__(self, data=data, units=units)
    #END DEF

    def __str__(self):
        """Returns a string represenation of the object"""
        return (self.StringPadding + "Final Measurement:\n" + Measurement.__str__(self) )
    #END DEF
#END CLASS





"""
------------------------------------------------------------------------
UDP_SERVERREPORT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single UDP Server Report
            (i.e. This object represent one line of text in a UDP test)
------------------------------------------------------------------------
"""


class UDP_ServerReport(Measurement):

    """Inherits Measurment, but adds a number of other attributes"""

    '''
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    TimeStart       = 0.0
    TimeEnd         = 0.0

    Size            = 0.0
    size_string     = ""
    size_units      = ""
    #_size_pad = ""

    Speed           = 0.0
    speed_string    = ""
    speed_units     = ""
    #_speed_pad = ""

    # ---- CLASS ATTRIBUTES ----
    Jitter          = 0
    Dtgrams_Lost    = 0
    Dtgrams_Sent    = 0
    Dtgrams_Perc    = 0
    Dtgrams_OoO     = 0
    # ------------------------------
    '''

    def __init__(self, data, units=("KBytes","Kbits/sec")):
        """
        Used to initialize an object of this class
        ARGS:
            self:   reference to the object calling this method (i.e. Java's THIS)
            data:   List of Strings, the Server Report that will be parsed for data
            units:  Tuple of two Strings, the units being used by the measurement
        """
        #Call the parent class' __init__
        Measurement.__init__(self, data=data[0], units=units)

        #Parsing out the remaining bits from the Server Report
        self.Jitter = float(data[0].split("/sec")[1].split("ms")[0].strip())

        #Calculating the percentage at the end of this server report string
        fraction = data[0].split("ms")[1].strip()
        lost = int(fraction.split("/")[0].strip())
        total = int(fraction.split("/")[1].split("(")[0].strip())
        self.Dtgrams_Lost = lost
        self.Dtgrams_Sent = total

        #The funny multiplication, division, and massive amounts of casting is
        # so that I get two decimal points worth of accuracy
        self.Dtgrams_Perc = float(int((float(lost)/float(total))*10000))/100
        #If there was another line after the Server Report, we want to parse the info from there
        if (len(data) != 1):
            self.Dtgrams_OoO = int(data[1].split("sec")[1].split("datagrams")[0].strip())
        else:
            self.Dtgrams_OoO = 0
    #END DEF

    def __str__(self):
        """Returns a string represenation of the object"""
        string = (self.StringPadding +
                  "Server Report:\n" +
                  Measurement.__str__(self) +
                  "   {}ms".format(self.Jitter) +
                  "   {}/{}".format(self.Dtgrams_Lost,self.Dtgrams_Sent) +
                  "  {}%".format(self.Dtgrams_Perc) +
                  (("\n" + self.StringPadding +
                    "{} datagrams received out-of-order".format(self.Dtgrams_OoO))
                   if (self.Dtgrams_OoO > 0) else ""
                   )
                  )
        return string
    #END DEF
#END CLASS
