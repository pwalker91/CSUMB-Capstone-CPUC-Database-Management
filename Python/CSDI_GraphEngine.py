#!/usr/local/bin/python3
"""
--------------------------------------------------------------------------------
CSDI GRAPHING DRIVER.PY

AUTHOR(S):  Peter Walker        pwalker@csumb.edu
            Nicholas Moradi     nmoradi@csumb.edu

PURPOSE-    This is going to be the main script called when analyses need to be
             processed. It will be run on a schedule, likely every 20 minutes.
--------------------------------------------------------------------------------
"""
#IMPORTS
import sys
import os
import shutil
import json
import hashlib
import traceback
from CSDI_MySQL import CSDI_MySQL as DB
from CSDI_matplotlib import barGraph
from sensitiveInfo import (PASSWORD, EMAIL_USER, EMAIL_PASS)
from EmailClient import EmailClient
#END IMPORTS


#We need to first connect to the necessary databases.
PageDB = DB(database='website', password=PASSWORD)
DataDB = DB(database='cpuc', password=PASSWORD)
PageDB.connect()
DataDB.connect()

#Checking to see if a folder path was passed in through sys args
if len(sys.argv)<2:
    imageFolder = "/home/ubuntu"
else:
    imageFolder = os.path.abspath(sys.argv[1])
    if not os.path.isdir(imageFolder):
        raise RuntimeError("Given directory is not a true directory")
#END IF/ELSE


#Our first step is to get all of the pages that have not been generated yet
EXECUTED, results_pageGen = PageDB.select("PageRequest", "*", IsGenerated=False)
page_headers, *PAGE_RESULTS = results_pageGen
#Now that we have our results, (initially, just one), we will go through each
# one and generate its image
newpageCount = 0
for PAGE in PAGE_RESULTS:
    #Making it easier to get the PageRequest row's ID
    requestPageID = PAGE[page_headers.index("Id")]

    #We want to skip any rows where an error was encountered
    if PAGE[page_headers.index("ErrorEncountered")]:
        continue

    #Lots of stuff enclosed in a TRY, so that we can update the 'PageRequest'
    # table on an error
    try:
        #We start by loading the JSON from the results of the query to 'PageRequest'
        TestJSON = json.loads( PAGE[page_headers.index("AnalysisOpts")].decode() )
        #print(TestJSON, end="\n\n")

        #Getting all of the files that match the given criteria
        EXECUTED, results_Files = DataDB.select('FileInfo', "*", **TestJSON['file_criteria'])
        if not EXECUTED:
            print("SOMETHING WENT WRONG!!  when getting fileInfo")
            continue
        #Splitting the headers from the actual results, then getting the ID and grouping
        # indexes, which I will use later
        file_headers, *FILE_RESULTS = results_Files
        IdInd = file_headers.index("Id")


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
            fileGroupingInd = ROW[file_headers.index(TestJSON['grouping_file'])]
            #If the category these results belong to does not yet have an array, then
            # we create it. We create it by getting the attribute of the file requested
            # in 'grouping_file', and combining it with the attribute of the test
            # specified in 'grouping_test'
            #For each result returned, get the value we want (based on JSON 'table_val')
            # and append it to the correct group
            for VAL_ROW in VAL_RESULTS:
                if TestJSON['grouping_test']:
                    testGroupingInd = VAL_ROW[val_headers.index(TestJSON['grouping_test'])]
                else:
                    testGroupingInd = ""
                GROUP_IND = "{} {}".format(fileGroupingInd, testGroupingInd)
                if GROUP_IND not in VALUES:
                    VALUES[GROUP_IND] = []
                VALUES[GROUP_IND].append( VAL_ROW[valInd] )
        #END FOR


        '''
        #This is just a test to see what is in the arrays that I want to use
        print(len(VALUES))
        for key in VALUES:
            print("{}: {}".format(key, len(VALUES[key])))
            types = {type(val) for val in VALUES[key]}
            print(types)
        #'''

        #Creating the image, and storing its path on the system
        imagePath = barGraph(VALUES)
        imagePath = shutil.move(imagePath, imageFolder)

        #Converting the data used into JSON
        dataJSON = json.dumps(VALUES)

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
                      Fid=requestPageID,
                      CalculatedData=dataJSON,
                      ImagePath=imagePath,
                      MetaInfo=metadataJSON,
                      PageHash=pageHash
                      )

        #Updating PageRequest with a TRUE in IsGenerated
        UPDATE = """UPDATE PageRequest
                    SET IsGenerated=1, ErrorEncountered=0
                    WHERE Id=%(ID)s
                 """
        UPDATE_DAT = {"ID":requestPageID}
        PageDB._CSDI_MySQL__executeQuery(UPDATE, UPDATE_DAT)

        #Send email to PAGE[page_headers.index("ContactEmail")]
        NAME = PAGE[page_headers.index("ContactName")]
        if not NAME:
            NAME = "CSDI User"
        EMAIL = PAGE[page_headers.index("ContactEmail")]

        ec = EmailClient(name='CSDI Server Bot', username=EMAIL_USER, password=EMAIL_PASS)
        ec.addRecipient( (NAME, EMAIL) )
        ec.SUBJECT = "CSDI Analysis Ready"
        ec.MESSAGE = ("Hello {},\n\n".format(NAME) +
                      "Your analysis request has been processed, " +
                      "and the results can be found at this link:\n\n" +
                      "http://54.200.224.217/csdi/results.php?h={}\n\n".format(pageHash) +
                      "If you have any questions regarding the analysis process, or the website" +
                      " itself, please do not hesitate to contact us.\n\n\n" +
                      "Sincerely,\n\n" +
                      "The CSDI Team"
                      )
        ec.send()

        newpageCount += 1
    #END TRY
    except:
        traceback.print_exc()
        #Updating PageRequest with a TRUE in IsGenerated
        UPDATE = """UPDATE PageRequest
                    SET ErrorEncountered=1
                    WHERE Id=%(ID)s
                 """
        UPDATE_DAT = {"ID":requestPageID}
        PageDB._CSDI_MySQL__executeQuery(UPDATE, UPDATE_DAT)
    #END TRY/EXCEPT
#END FOR

print("Script Complete. {} pages generated.".format(newpageCount))
