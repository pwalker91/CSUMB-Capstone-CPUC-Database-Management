#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
CSDI GRAPHING DRIVER.PY

AUTHOR(S):  Peter Walker        pwalker@csumb.edu
    (kinda) Nicholas Moradi     nmoradi@csumb.edu
 
PURPOSE-    This is going to be the main script called
--------------------------------------------------------------------------------
"""
#IMPORTS
import sys
import json
import hashlib
from CSDI_MySQL import CSDI_MySQL as DB
from CSDI_matplotlib_adv import CSDI_MPL
#from CSDI_matplotlib_adv import CSDI_MPL as mpl
#END IMPORTS


#We need to first connect to the necessary databases.
PageDB = DB(database='CapStone', password='root')
DataDB = DB(database='testdb', password='root')
PageDB.connect()
DataDB.connect()

#Our first step is to get all of the pages that have not been generated yet
EXECUTED, results_pageGen = PageDB.select("PageRequest", "*", IsGenerated=False)
page_headers, *PAGE_RESULTS = results_pageGen

#Now that we have our results, (initially, just one), we will go through each
# one and generate its image
newpageCount = 0
for PAGE in PAGE_RESULTS:
    TestJSON = json.loads( PAGE[page_headers.index("AnalysisOpts")].decode() )

    '''
    TestJSON = { 'table':'TCPResults',
                 'table_val':'DownSpeed',
                 'file_criteria': { 'Date': '2014-05-05',
                                    'Date_COMP': '<='
                                    },
                 'test_criteria': { 'DownSpeed':100,
                                    'DownSpeed_COMP':">="
                                    },
                 'grouping': "NetworkCarrier",
                 'statistics': 'mean'
                 }
    TestJSON2 = json.dumps(TestJSON)
    TestJSON = json.loads(TestJSON2)
    '''

    #Getting all of the files that match the given criteria
    EXECUTED, results_Files = DataDB.select('FileInfo', "*", **TestJSON['file_criteria'])
    if not EXECUTED:
        print("SOMETHING WENT WRONG!!  when getting fileInfo")
        continue
    #Splitting the headers from the actual results, then getting the ID and grouping
    # indexes, which I will use later
    file_headers, *FILE_RESULTS = results_Files
    IdInd = file_headers.index("Id")
    groupingInd = file_headers.index(TestJSON['grouping'])


    #Now we will actually get the results from the requested table
    VALUES = {}
    for ROW in FILE_RESULTS:
        EXECUTED, results_Vals = DataDB.select(TestJSON['table'], "*", Oid=ROW[IdInd], **TestJSON['test_criteria'])
        if not EXECUTED:
            print("SOMETHING WENT WRONG!!  when getting Test info")
            continue
        #Again, splitting headers from results
        val_headers, *VAL_RESULTS = results_Vals
        valInd = val_headers.index(TestJSON['table_val'])
        #If the category these results belong to does not yet have an array, then
        # we create it
        if ROW[groupingInd] not in VALUES:
            VALUES[ROW[groupingInd]] = []
        #For each result returned, get the value we want (based on JSON 'table_val')
        # and append it to the correct group
        for VAL_ROW in VAL_RESULTS:
            VALUES[ROW[groupingInd]].append( VAL_ROW[valInd] )
    #END FOR


    '''
    This is just a test to see what is in the arrays that I want to use

    for key in VALUES:
        print("{}: {}".format(key, len(VALUES[key])))
        types = {type(val) for val in VALUES[key]}
        print(types)
    '''
    
    dataToGraph = CSDI_MPL()
    dataToGraph.barGraph(VALUES)
    

    #Converting the data used into JSON
    """dataJSON = json.dumps(VALUES)

    #Some metadata on the data used to create the graph
    metadata = {}
    metadata['columnNames'] = list(VALUES.keys())
    metadata['filesUsed'] = len(FILE_RESULTS)
    metadata['dataPoints'] = sum( [len(VALUES[col]) for col in VALUES] )
    metadataJSON = json.dumps(metadata)

    #Creating the page link from the row ID
    md5 = hashlib.md5()
    md5.update( str(PAGE[page_headers.index("Id")]).encode() )
    pageHash = md5.hexdigest()[:10]

    #Finally inserting our information into the PageResult page
    PageDB.insert("PageResults",
                  CalculatedData=dataJSON,
                  ImagePath="/a/s/d/f/image.jpg",
                  MetaInfo=metadataJSON,
                  PageHash=pageHash
                  )

    #Updating PageRequest with a TRUE in IsGenerated
    UPDATE = "UPDATE PageRequest
                SET IsGenerated=1
                WHERE Id=%(ID)s
             "
    UPDATE_DAT = {"ID":PAGE[page_headers.index("Id")]}
    PageDB._CSDI_MySQL__executeQuery(UPDATE, UPDATE_DAT)"""

    #Send email to PAGE[page_headers.index("ContactEmail")]

    newpageCount += 1
#END FOR

print("Script Complete. {} pages generated.".format(newpageCount))
