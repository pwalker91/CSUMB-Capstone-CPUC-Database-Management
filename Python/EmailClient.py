#!/usr/local/bin/python3
"""
------------------------------------------------------------------------
EMAIL CLIENT.PY

AUTHOR(S):     Peter Walker    pwalker@csumb.edu
               Zac Leids       zleids@csumb.edu

PURPOSE-  This module provides a class (EmailClient) that will send
            and email as CPUC Server, with the given files attached.
            Meant to be used on the live CPUC servers
------------------------------------------------------------------------
"""
#IMPORTS
import ssl
import smtplib
import sys
import os
import traceback
import mimetypes
import datetime
from base64 import (b64encode, b64decode)
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText



class EmailClient(object):

    """
    A class that tracks email user settings, message values, and does some
     error checking of new recipients. Main function to-be-used is send()
    """

    def __init__(self, **kwargs):
        """Basic class initialization"""
        self.recipients = {"To": [],
                           "Cc": [],
                           "Bcc":[] }
        self.MESSAGE = ""
        self.SUBJECT = ""
        self.ATTACHMENTS = []

        self.cfg = {"server":    "smtp.gmail.com",
                    "name":      "Automated Server",
                    "username":  ""
                    }
        self.__PAZZWORD = "password"
        if "password" in kwargs:
            self.__PAZZWORD = kwargs['password']
            del kwargs['password']
        self.cfg.update(kwargs)
    #END DEF


# Special functions for formatting emails --------------------------------------

    def __checkEmailInfoArgs(func):
        def checkInfoWrapper(*args, **kwargs):
            addressPairs = list(args)[1:]
            for pair in addressPairs:
                if not args[0].__checkEmailInfo(pair):
                    raise ValueError("The addresses provided are not in the correct format.\n"+
                                     "Emails should come in a tuple, with the first element a "+
                                     "NAME, and second an EMAIL ADDRESS.\n"+
                                     "Was given '{}', '{}'".format(*pair))
            return func(*args, **kwargs)
        #END DEF
        return checkInfoWrapper
    #END DEF

    def __checkEmailInfo(self, info):
        """
        Check given email information is in the correct format.

        ARGS:
            info    List/Tuple, in the format [name, email address]
        RETURNS:
            Boolean True, if in correct format, False otherwise
        """
        if isinstance(info, (list,tuple)):
            if not isinstance(info[0], str) and not isinstance(info[1], str):
                return False
            if "@" not in info[1] and "." not in info[1][-5:]:
                return False
            return True
        else:
            return False
    #END DEF

    def __makeAddressField(self, elems):
        """
        Creating a string of email addresses from the elements passed in.

        ARGS:
            elems   A list of elements to convert into a MIME address field. The information
                     is run through __checkEmailInfo() for correctness
        RETURNS:
            String, the address field requested as a single string
        """
        fieldsAsString = ""
        for elem in elems:
            if not self.__checkEmailInfo(elem):
                raise ValueError("The addresses provided are not in the correct format")
            fieldsAsString += elem[0]+" <"+elem[1]+">, "
        return fieldsAsString[:-2]
    #END DEF

    def __makeAttachment(self, FILELOCATION):
        """Returns a MIME attachment object"""
        ctype, encoding = mimetypes.guess_type(FILELOCATION)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        #Getting the type of file that we are working with
        maintype, subtype = ctype.split("/", 1)
        #Based on maintype, we will use different MIME wrappers. Each block determines
        # what type of file we are currently looking at, opens the file, and reads it
        # in to the appropiate MIME object
        with open(FILELOCATION, "r", encoding='utf-8') as fp:
            if maintype == "text":
                attachment = MIMEText(fp.read(), _subtype=subtype)
            elif maintype == "image":
                attachment = MIMEImage(fp.read(), _subtype=subtype)
            elif maintype == "audio":
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
            else:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)
        #And here, we finally attach the file
        attachment.add_header("Content-Disposition", "attachment", filename=os.path.basename(FILELOCATION))
        return attachment
    #END DEF


# Functions for defining and sending an email ----------------------------------

    @__checkEmailInfoArgs
    def addRecipient(self, *args, **kwargs):
        """
        Takes the given name/address pairs in args, and adds them to the correct
         recipients field.
        ARGS:
            'args' will become a list of inputs, which should be Tuples of two Strings, the
             name and email address of the intended recipients.
        KWARGS:
            field   String, the email field (either 'To', 'Cc', 'Bcc') to add the recipient to
        RAISES:
            ValueError if the given field in kwargs['field'] is not in the object's
             list of fields.
        """
        #If kwargs['field'] is set, then we are going to add the given addresses to that
        # field. Otherwise, we add the given addresses to self.recipients["To"]
        if "field" in kwargs:
            if kwargs['field'] in self.recipients:
                for info in args:
                    self.recipients[kwargs["field"]].append(info)
            else:
                raise ValueError("You cannot add a recipient to this field. "+
                                 "Was given '{}'".format(kwargs["field"]))
        else:
            for info in args:
                self.recipients["To"].append(info)
        #END IF/ELSE
        return True
    #END DEF

    @__checkEmailInfoArgs
    def removeRecipient(self, *args):
        """
        This will go through each name/address pair given in args, and remove
         it from all field in self.recipients
        ARGS:
            'args' should become a list of recipients, which should be Tuples of two Strings, the
             name and email address of the intended recipients.
        """
        for pair in args:
            #We need to go through each field in self.recipients, and then check
            # each savedPair in that field. If the emails match, then we remove the savedPair
            for field in self.recipients:
                for index, savedPair in enumerate(self.recipients[field]):
                    if pair[1]==savedPair[1]:
                        self.recipients[field].pop(index)
            #END FOR
        #END FOR pair
        return True
    #END DEF

    def removeAllRecipients(self):
        """Removes all intended recipients from every field"""
        for field in self.recipients:
            self.recipients[field] = []
        return True
    #END DEF

    def addAttachment(self, *args):
        """
        Takes a number of files in 'args', and creates all of the attachment objects
        ARGS:
            unknown number of file paths (no keywords)
        """
        for item in args:
            if isinstance(item, str) and os.path.isfile(item):
                self.ATTACHMENTS.append(self.__makeAttachment(item))
        return True
    #END DEF

    def __makeMessage(self):
        #Initializing our message object, and setting some cursory information, like
        # the From field an subject
        EMAILMESSAGE = MIMEMultipart()

        #Setting some of the message information if the object's attributes
        # are currently empty
        datetimeSent = datetime.datetime.now().strftime("%H:%M:%S %a, %b %d, %Y")
        if not self.SUBJECT:
            SUBJECT = "Automated Email - {}".format(datetimeSent.split(" ",1)[1])
            EMAILMESSAGE['Subject'] = SUBJECT
        else:
            EMAILMESSAGE['Subject'] = self.SUBJECT
        if not self.MESSAGE:
            MESSAGE = "Automated Email - {}".format(datetimeSent.split(" ",1)[1])
            body = ("This email has {} items attached.\n".format( len(self.ATTACHMENTS) )+
                    "This message was generated at {}.".format( datetimeSent ))
            EMAILMESSAGE.attach(MIMEText(body))
        else:
            EMAILMESSAGE.attach(MIMEText(self.MESSAGE))
        #END IF/ELSEs
        EMAILMESSAGE['From'] = "{} <{}>".format(self.cfg['name'], self.cfg['username'])

        #Generating the necessary strings to include in the EMAILMESSAGE object, which
        # dictate the content of the message. However, we also need an array of email
        # addresses for the smtplib function that actually send the email.
        RECIPIENTS = []
        for recip in self.recipients["To"]:
            RECIPIENTS.append(recip[1])
        EMAILMESSAGE['To'] = self.__makeAddressField(self.recipients["To"])
        #END FOR
        for recip in self.recipients["Cc"]:
            RECIPIENTS.append(recip[1])
        EMAILMESSAGE['Cc'] = self.__makeAddressField(self.recipients["Cc"])

        #Attaching the file to the message. There are a few checks for message type.
        for attachment in self.ATTACHMENTS:
            EMAILMESSAGE.attach(attachment)
        #END FOR

        return EMAILMESSAGE, RECIPIENTS
    #END DEF

    def send(self, *args, **kwargs):
        """
        Using the object attributes 'recipients', 'MESSAGE', 'SUBJECT', and
         'ATTACHMENTS', sends an email
        ARGS:
            None
        RETURNS:
            None
        RAISES:
            None. Prints error message if email was not sent
        """
        EMAILMESSAGE, RECIPIENTS = self.__makeMessage()

        #Finally sending the email
        with smtplib.SMTP( self.cfg['server'] ) as server:
            try:
                #server.set_debuglevel(1)
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.login(self.cfg['username'], self.__PAZZWORD)

                #Sending the email, as 'EMAIL_USER', to the given addresses. The message is a string
                # version of the MIMEMultipart object created previously
                server.sendmail(self.cfg['username'], RECIPIENTS, EMAILMESSAGE.as_string())

                #This block is so that we can actually BCC someone. sendmail() does not
                # automatically take care of this
                #To do this, we add the BCC addresses to allRecipients, and also add
                # the formatted measurements to the MIME object's 'Bcc' attribute.
                # Once that is done, we send the message
                if len(self.recipients["Bcc"]):
                    #allRecipients needs to be empty so we don't email twice
                    RECIPIENTS = []
                    for recip in self.recipients["Bcc"]:
                        RECIPIENTS.append(recip[1])
                    EMAILMESSAGE['Bcc'] = self.__makeAddressField(self.recipients["Bcc"])
                    server.sendmail(self.cfg['username'], RECIPIENTS, EMAILMESSAGE.as_string())
                #END IF
                print("Message Sent")
                server.close()
                return True
            except:
                exctype, value, traceb = sys.exc_info()
                traceback.print_exception(exctype, value, traceb)
                print("Message was not Sent")
                server.close()
                return False
        #END WITH
    #END DEF
#END CLASS
