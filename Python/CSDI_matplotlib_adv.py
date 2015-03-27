import matplotlib.pyplot as plt
import sys
import os
import pymysql
import numpy as np
import statistics
from pylab import *
from CSDI_MySQL import CSDI_MySQL #talk to them
"""VALUES = { "AT&T": [53876, 47494, 41592, 41047, 39693, 39305, 38401, 35161, 33825, 33593],
           "Verizon": [25849, 19277, 29143, 20132, 37537, 17897, 32903, 20714, 20551, 20781],
           "T-Mobile": [16960,11128,14667,9900,21068,15284,24122,20548,32936,20866],
           "Sprint": [1255, 1103, 4394, 3192, 560, 410.9, 955, 259, 199.2]
         }"""
STDEVs = []
"""or
for key in VALUES:
    STDEVs[key] = statistics.pstdev(VALUES[key])
    MEANS[key] = statistics.mean(VALUES[key])
"""

class CSDI_MPL():
    #barGraph that has mean and I bars for standard deviation
    def barGraph(self, data):
        #this shows the value of mean at the top of the bar graph for each provider
        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                        ha='center', va='bottom')
        #if I am only worried about speeds and providers is this ok?
        #new objective find out how to create graphs dynamically
        #but for now this will work
        N = 1
        providers = []
        speeds = []
        """for keys, vals in data.items():
            STDEVs.append(statistics.pstdev(vals))
            providers.append(keys)
            speeds.append(vals)"""
        fig, ax = plt.subplots()
        width = .35
        ind = np.arange(N)
        """num_of_graphs = len(providers)
        print (num_of_graphs)
        graph = [num_of_graphs]
        for i in range(num_of_graphs):
            for key, val in data.items():
                graph[i] = ax.bar(ind, statistics.mean(vals) , width, color = 'b', yerr = statistics.pstdev(vals))"""
        #this ^^^^^^^^^^^^ is my biggest issue:
        #"AssertionError: incompatible sizes: argument 'height' must be length 1 or scalar"
        #main part to create graph...
        #if graphs are only providers/speeds, this will work fine however, looking to make it more automated and less hardcoded. 
        speed_tuple = tuple(tuple(x) for x in speeds)
        stdev_tuple = tuple(STDEVs)
        for keys, vals in data.items():
            if keys == 'AT&T':
                graph1 = ax.bar(ind, statistics.mean(vals) , width, color = 'b', yerr = statistics.pstdev(vals))
            if keys == 'Verizon':
                graph2 = ax.bar(ind+width, statistics.mean(vals), width, color = 'r', yerr = statistics.pstdev(vals))
            if keys == 'Sprint':
                graph3 = ax.bar(ind+(2*width), statistics.mean(vals), width, color = 'y', yerr = statistics.pstdev(vals))
            if keys == 'T-Mobile':
                graph4 = ax.bar(ind+ (3 * width), statistics.mean(vals), width, color = 'm', yerr = statistics.pstdev(vals))
        ax.set_ylabel('Speeds')
        ax.set_title('Mean of Speeds with standard deviation grouped by Provider')
        ax.set_xticks(ind/4)
        #provides a legend to distinguish graphs
        ax.legend((graph1[0], graph2[0], graph3[0], graph4[0]), ('AT&T', 'Verizon', 'Sprint', 'T-Mobile'))
        #tried setting tick labels at the bottom, however not working
        ticklabels = ""
        for key in providers:
            ticklabels += "'{}', ".format(key)
        ticklabels = "(" + ticklabels[:-2] + ")"
        ax.set_xticklabels(ticklabels)

        autolabel(graph1)
        autolabel(graph2)
        autolabel(graph3)
        autolabel(graph4)
        plt.savefig("MeanSpeeds_vs_Providers.png")
        filepath = os.path.join(os.getcwd(), "MeanSpeeds_vs_Providers.png")
        plt.show()
        print (filepath)
        return filepath




