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

# IMPORTS
from PyObjects.__Base import Formatting
#END IMPORTS




"""
------------------------------------------------------------------------
MEASUREMENT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single measurement of data transfer speed in a single test
            (i.e. This object represent one line of text in a speed test)

VARIABLES:
    TimeStart       Float, represents the start time of this Ping
    TimeEnd         Float, represents the end time of this Ping (should always be start + 1)
    Size            Float, represents this Ping's size in Kbits sent
    size_string     String, converted from size, used in __str__
    size_units      String, units to be appended to string
    Speed           Float, represents this Ping's speed in KBytes/sec
    speed_string    String, converted from speed, used in __str__
    speed_units     String, units to be appended to string

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
                    data:   String, the measurement that will be parsed for data
                    units:  Tuple of two Strings, the units being used by the measurement
        OUTPUTS-    none
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
-----------------------------------------------------------------------
"""

# CLASS
class Measurement(Formatting):
    # ----------------------------------
    # Class attributes
    TimeStart       = 0
    TimeEnd         = 0

    Size            = 0
    size_string     = ""
    size_units      = ""
    #_size_pad = ""

    Speed           = 0
    speed_string    = ""
    speed_units     = ""
    #_speed_pad = ""
    # ----------------------------------

    # DESC: Initializing class
    def __init__(self, data, units=("KBytes","Kbits/sec")):
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

        #!! ALL CODE BELOW IS PURELY FOR NICE PRINTOUTS !!
        #This section adds trailing decimal zeros following the speed and size numbers, as sometimes
        # the size may vary between ##.# and ###
        if ("." in data_size):
            if (len(data_size.split(".")[1]) == 1):
                data_size += "0"
            #END IF
        else:
            data_size += ".00"
        self.size_string = str(self.Size)
        if ("." in data_speed):
            if (len(data_speed.split(".")[1]) == 1):
                data_speed += "0"
            #END IF
        else:
            data_speed += ".00"
        self.speed_string = str(self.Speed)

        #Creating the padding of spaces needed to line up all of the numbers
        # The padding after the time varies because the time may be between 0 and 99.
        # If the start and end are both 1 digit, two spaces are needed. If start and end are
        #  a 1 and 2 digit number, one space is needed
        self.time_pad = ""
        if self.TimeEnd < 10.0:
            self.time_pad = "  "
        elif self.TimeStart < 10.0 and self.TimeEnd >= 10.0:
            self.time_pad = " "

        from math import log10
        self._size_pad = (" " * (4 - int(log10(self.Size)))) if self.Size else (" " * 4)
        self._speed_pad = (" " * (4 - int(log10(self.Speed)))) if self.Speed else (" " * 4)
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (self.StringPadding +
                str(self.TimeStart) + "-" + str(self.TimeEnd) + " sec" + self.time_pad + "  "
                    + self._size_pad + self.size_string + " " + str(self.size_units) + "  "
                    + self._speed_pad + self.speed_string + " " + str(self.speed_units)
               )
    #END DEF
#END CLASS





"""
------------------------------------------------------------------------
FINAL_MEASUREMENT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single measurement of data transfer speed in a single test
            (i.e. This object represent one line of text in a speed test)

VARIABLES:
  INHERITED
    TimeStart       Float, represents the start time of this Ping
    TimeEnd         Float, represents the end time of this Ping (should always be start + 1)
    Size            Float, represents this Ping's size in Kbits sent
    size_string     String, converted from size, used in __str__
    size_units      String, units to be appended to string
    Speed           Float, represents this Ping's speed in KBytes/sec
    speed_string    String, converted from speed, used in __str__
    speed_units     String, units to be appended to string

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
                    data:   String, the measurement that will be parsed for data
                    units:  Tuple of two Strings, the units being used by the measurement
        OUTPUTS-    none
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
-----------------------------------------------------------------------
"""

# CLASS
class Final_Measurement(Measurement):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # timeStart       = 0
    # timeEnd         = 0
    # size            = 0
    # size_string     = ""
    # size_units      = ""
    # _size_pad = ""
    # speed           = 0
    # speed_string    = ""
    # speed_units     = ""
    # _speed_pad = ""

    # Class attributes
    # ----------------------------------

    # DESC: Initializing class
    def __init__(self, data, units=("KBytes","Kbits/sec")):
        Measurement.__init__(self, data=data, units=units)
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        return (self.StringPadding + "Final Measurement:\n" + Measurement.__str__(self) )
#END CLASS





"""
------------------------------------------------------------------------
UDP_SERVERREPORT Class

AUTHOR(S):    Peter Walker    pwalker@csumb.edu

PURPOSE:    Holds a single UDP Server Report
            (i.e. This object represent one line of text in a UDP test)

VARIABLES:
  INHERITED
    TimeStart       Float, represents the start time of this Ping
    TimeEnd         Float, represents the end time of this Ping (should always be start + 1)
    Size            Float, represents this Ping's size in Kbits sent
    size_string     String, converted from size, used in __str__
    size_units      String, units to be appended to string
    Speed           Float, represents this Ping's speed in KBytes/sec
    speed_string    String, converted from speed, used in __str__
    speed_units     String, units to be appended to string
  NOT INHERITED
    Jitter          Float, the jitter of the UDP test
    Dtgrams_Lost    Integer, number of datagrams lost in test
    Dtgrams_Sent    Integer, number of datagrams sent
    Dtgrams_Perc    Float, percent of datagrams lost in test
    Dtgrams_OoO     Integer, number of datagrams received out of order

FUNCTIONS:
    __init__ - Used to initialize an object of this class
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
                    data:   List of Strings, the Server Report that will be parsed for data
                    units:  Tuple of two Strings, the units being used by the measurement
        OUTPUTS-    none
    __str__ - Returns a string represenation of the object
        INPUTS-     self:   reference to the object calling this method (i.e. Java's THIS)
        OUTPUTS-    String, representing the attributes of the object (THIS)
-----------------------------------------------------------------------
"""

# CLASS
class UDP_ServerReport(Measurement):
    # ------------------------------
    # ---- INHERITED ATTRIBUTES ----
    # timeStart       = 0
    # timeEnd         = 0
    # size            = 0
    # size_string     = ""
    # size_units      = ""
    # _size_pad = ""
    # speed           = 0
    # speed_string    = ""
    # speed_units     = ""
    # _speed_pad = ""

    # Class attributes
    Jitter          = 0
    Dtgrams_Lost    = 0
    Dtgrams_Sent    = 0
    Dtgrams_Perc    = 0
    Dtgrams_OoO     = 0
    # ----------------------------------

    # DESC: Initializing class
    def __init__(self, data, units=("KBytes","Kbits/sec")):
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
    #END DEF

    # DESC: Creating a string representation of our object
    def __str__(self):
        string = (self.StringPadding +
                    "Server Report:\n" +
                        Measurement.__str__(self) +
                            "   " + str(self.Jitter) + "ms" +
                            "   " + str(self.Dtgrams_Lost) + "/" + str(self.Dtgrams_Sent) +
                            "  " + str(self.Dtgrams_Perc) + "%" +
                            (("\n" + self.StringPadding +
                                str(self.Dtgrams_OoO) + " datagrams received out-of-order")
                                if (self.Dtgrams_OoO > 0) else "")
                  )
        return string
    #END DEF
#END CLASS
