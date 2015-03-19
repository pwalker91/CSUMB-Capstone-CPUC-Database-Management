import matplotlib.pyplot as plt
import sys
import pymysql
import numpy as np
from statistics import mean
from pylab import *
from CSDI_MySQL import CSDI_MySQL #talk to them

class CSDI_MPL(self, data):
    def getQueryResults():
        results = db.select('test', "speed","provider", "id", speed="0", speed_operator=">")
        print (results)
        dataForGraph(results)

    def dataForGraph(results):
        #init lists to store data pertaining to specific providers speed and id, this is the y axis
        atemp = []
        vtemp = []
        ttemp = []
        stemp = []
        #init list to store id, this will be our x axis that we go off of.
        aid = []
        vid = []
        tid = []
        sid = []
        #%id and %temp grabs the necessary information from results and stores it
        #reason for no provider is because of for loop already organizing it. This was a bit tricky
        for records in results[1]:
            if (records[1] == 'att'):
                atemp.append(records[0])
                aid.append(records[2])
            if (records[1] == 'verizon'):
                vtemp.append(records[0])
                vid.append(records[2])
            if (records[1] == 't-mobile'):
                ttemp.append(records[0])
                tid.append(records[2])
            if (records[1] == 'sprint'):
                stemp.append(records[0])
                sid.append(records[2])
        lineGraph(atemp, aid, vtemp, vid, ttemp, tid, stemp, sid)
    def lineGraph(att, attid, verizon, verizonid, tmobile, tmobileid, sprint, sprintid):
    
        #because of the way graph material is set up we use %id as x and %temp as y
        #labeled them and colored them according to their marketing colors. IE Att is blue and white
        #currently trying to create x_labels and y_labels. however in order to do that I will need to rearrange code
        plt.plot(attid, att, color = 'b', marker = 'o', label = 'att')
        plt.plot(verizonid, verizon, color = 'r', marker = '*', label = 'verizon')
        plt.plot(tmobileid, tmobile, color = 'm', marker = '^', label = 't-mobile')
        plt.plot(sprintid, sprint, color = 'y', marker = 'x', label = 'sprint')
        title('Speed By Provider')
        grid(True)
        plt.draw()
        #adds legend
        plt.legend()
        plt.show()
        F = gcf()
        DPI = F.get_dpi()
        F.savefig('line.png', dpi = (80))


lineGraph()
#barGraph()