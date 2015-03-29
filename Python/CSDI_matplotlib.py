#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
CSDI MATPLOTLIB.PY

AUTHOR(S):  Peter Walker        pwalker@csumb.edu
            Nicholas Moradi     nmoradi@csumb.edu

PURPOSE-    This is going to be the main script called
--------------------------------------------------------------------------------
"""

#IMPORTS
import sys
import os
import numpy as np
import statistics
import datetime
import matplotlib.pyplot as plt
#END IMPORTS




def _getCarrierColor(name):
    """Given a string in name, sees if any substrings are one of the carrier names"""
    providerColor = {"AT&T":    "#144acc",
                     "VERIZON": "#c11010",
                     "SPRINT":  "#e2ee2e",
                     "T-MOBILE":"#ab00da",
                     "OTHER":   "#969696" }
    substrs = [sub.upper() for sub in name.split(" ")]
    for subby in substrs:
        if subby in providerColor:
            return providerColor[subby]
    return providerColor["OTHER"]
#END DEF


def barGraph(DATA, savePath=""):
    """This takes a dictionary of arrays, and graphs them with matplotlib"""
    #this shows the value of mean at the top of the bar graph for each provider
    def autolabel(rect):
        """For adding the height of our retangle to its top"""
        #Getting the location of the middle of the top edge of our rectangle, where
        # our text will go
        height = rect.get_height()
        xCoord = rect.get_x()
        width = rect.get_width()
        ax.text(xCoord+(width/2.0), 1.05*height,
                str(int(height)),
                ha='center', va='bottom')
        return True
    #END DEF

    #We first start by making a plot, and setting some "global" values
    fig, ax = plt.subplots()
    rectWidth = 1.0/len(DATA)
    allGraphs = {"Bars":  [],
                 "Names": [] }
    #This is for the "X" coordinate of our rectangle, which should be 0,
    # so we make an array of just a zero.
    ind = np.arange(1)

    #Now that we have our graph, we are going to go through our data, which should
    # be composed of an index (the name of the data) and an array of values.
    numGen = 0
    orderedKeys = sorted(DATA.keys())
    for key in orderedKeys:
        myColor = _getCarrierColor(key)
        BARS = ax.bar(left=ind + ((numGen-1)*(rectWidth*0.8)),
                      height=statistics.mean(DATA[key]),
                      width=rectWidth,
                      bottom=None,
                      color=myColor,
                      yerr=statistics.pstdev(DATA[key]))
        allGraphs['Bars'].append(BARS[0])
        allGraphs['Names'].append(key)
        numGen += 1
    #END FOR
    ax.set_ylabel('Average Throughput')
    ax.set_title('Throughput Mean and Standard Deviation')
    ax.set_xticks(ind/len(DATA))
    #Adding in the legend, based on the graphs and names stored in 'allGraphs'
    ax.legend(tuple(allGraphs["Bars"]),
              tuple(allGraphs['Names']))
    '''
    #tried setting tick labels at the bottom, however not working
    ticklabels = ""
    for key in providers:
        ticklabels += "'{}', ".format(key)
    ticklabels = "(" + ticklabels[:-2] + ")"
    ax.set_xticklabels(ticklabels)
    '''

    for bar in allGraphs['Bars']:
        autolabel(bar)

    ## savePath = os.path.join("/where/we/want/to/save/the", 'image.png')
    #For now, we will just save the image in the current working directory
    saveName = "{}.png".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S_%f"))
    plt.savefig(saveName, papertype='letter')
    savedFilePath = os.path.join(os.getcwd(), saveName)

    return savedFilePath
#END DEF
