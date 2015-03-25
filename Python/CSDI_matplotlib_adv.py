import matplotlib.pyplot as plt
import sys
import pymysql
import numpy as np
import statistics
from pylab import *
from CSDI_MySQL import CSDI_MySQL #talk to them


class CSDI_MPL(self):
    #barGraph that has mean and I bars for standard deviation
    def barGraph(self, values):
        graph values
        self.__saveFile("new_file_path.jpg")

    def __saveFile(self, graph, filePath):
        if not os.path.isfile(filePath):
            graph.save(filePath)
        else:
            filePath += "_ver2"



object = CSDI_MPL()
object.barGraph(values)
