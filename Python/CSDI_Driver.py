import sys
from CSDI_MySQL import CSDI_MySQL as db#talk to them
from CSDI_matplotlib_adv.py import CSDI_MPL as mpl

"""grabbed this from your query page:
    "{"form_ttype":"TCP","form_ttype_tcp_vals":"throughput","form_ttype_udp_vals":"","form_ttype_png_vals":"","form_date":"2015-01-23","form_date_comparator":"<=","form_stats":"median","form_submit":""}"
    for form_ttype is that the table that I will be querying? if not, what table am I grabbing from.
    does throughput mean speed? that sounds kinda stupid but just making sure
    """
#is it possible to write the select statement as a string? and feed the string to CSDI_MySQL?
myDict = {'table':'test', 'type': 'TCP', 'date': 'somedate', 'operator': '>=', 'statistics': 'mean'}

def getData(myDict):
    for data in myDict:
        #make values from myDict into the form where I can do results = db.select(information from my dict)
        #can i make it all one string and place it into select?
        #cause I want to do it kinda like how we did for select where we initiated query and added to it...
        print (data)
    #print (query)
    results = db.select("""information from myDict""")
    graphData(results)
def graphData(data):
    mpl.lineGraph(data)
    mpl.barGraph(data)
    #right? ^^^^?

