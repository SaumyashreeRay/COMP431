# from socket import*               # Import socket module
import sys

# serverName = sys.argv[1]
# serverPort = sys.argv[2]

# clientSocket = socket(AF_INET,SOCK_STREAM)
# clientSocket.connect((serverName, serverPort))

# print clientSocket.recv(1024)
# clientSocket.close                     # Close the socket when done

import socket               # Import socket module

#This function parses though the mailbox, checking if there is "@", 
#splitting it into local part and domain, and checking the validity of 
#the two
errorMessage = ""

def parseMailbox(mailbox):
    if mailbox.find('@') == -1:
    	errorMessage = "The email address is missing @"
    localPart, domain = mailbox.split("@",1)
    domain2 = domain.strip()     #domain cannot contain spaces before and after
    if(domain2 != domain):
        errorMessage = "The domain does not conform to SMTP standards"
    if parseLocalPart(localPart) is False:
        errorMessage = "The local part does not conform to SMTP standards"
    if parseDomain(domain) is False:
        errorMessage = "The domain does not conform to SMTP standards" 
    if endsWithCRLF(mailbox) is False:
        errorMessage = "Need to end with <enter>"
    else:
        errorMessage = "None"
    return errorMessage

#This function parses through the domain, searching for any existing invalid
#elements such as non alphanumeric characters with the exception of "."
#if "." is found in the string, then the string is split and recursively checked     
def parseDomain(domain):
    if domain.find(" ") != -1:
        return False
    if domain.find(".") != -1:
        elem, dom = domain.split(".",1)
        if parseElement(elem) is True and parseDomain(dom) is True:
            return True
    if parseElement(domain) is True:
        return True
    else:
        return False 

#This function parses through the local part, checking that there are no spaces
#and that everything is a valid char/string
def parseLocalPart(localPart):
    #check if everything is input string
    if localPart.find(" ") != -1:
        return False
    if isChar(localPart) is True:
        return True
    else:
        return False 
      
#This function exists as a stepping stone from element to name, following the grammar provided
def parseElement(element):
    if parseName(element) is True:
        return True
    else:
        return False

#This function checks if name is valid. Name has to be size 2 or more.
#and the first element has to be alphabetic
def parseName(name):
    if len(name) < 2:
        return False
    if name[0].isalpha() is True:
        if isLetterDigitString(name) is True: #rest have to be letter digit string
            return True
        
def isLetterDigitString(s):  #a letter digit string is alphanumeric
    return aOrD(s)

def isChar(s): #chars are ascii, but don't include special characters or spaces
    if isAscii(s) is True:
        if isSpecial(s) is False and s.find(" ") == -1:
            return True
    else:
        return False

def isAscii(text): #ascii values range from 0 to 127. Guidance for this method came from: http://stackoverflow.com/questions/196345/how-to-check-if-a-string-in-python-is-in-ascii
    return all(ord(c) < 128 for c in text)

def aOrD(s):
    return s.isalnum()

#This function checks to see if the given string contains any special characters                 
def isSpecial(s):
    return (s.find("<") != -1 or 
    s.find(">") != -1 or s.find("(") != -1 or 
    s.find(")") != -1 or s.find("[") != -1 or
    s.find("]") != -1 or s.find("\\") != -1 or 
    s.find(".") != -1 or s.find(",") != -1 or 
    s.find(";") != -1 or s.find(":") != -1 or 
    s.find("@") != -1 or s.find("'") != -1)

# Checks to see if given parameter ends with \n
def endsWithCRLF(dat):   
    if "\n" == dat[-1] is False:
        return False
    else:
        return True

def extractEmail(email):
    if checkCommand(email) == 1:
        email = email[5:-1]
    if checkCommand(email) == 2:
        email = email[3:-1]
    return email.strip()

def checkCommand(cmd):
    if cmd.find("\t") != -1:
        cmd = cmd.replace("\t", " ")

    if cmd[:5] == "From:":
        return 1
    if cmd[:3] == "To:":
        return 2
    if cmd[:8] == "Subject:":
    	return 3
    else:
        return 0

# This method parses the rcpt to cmd and calls on the parsePath() method if necessary
def parseRcptToCmd(entry_rcpttocmd):
    rcpt = entry_rcpttocmd[:4]
    if rcpt != "RCPT":
        print "500 Syntax error: command unrecognized"
        return False
    if entry_rcpttocmd.find("TO:") == -1:
        print "500 Syntax error: command unrecognized"
        return False
    if (entry_rcpttocmd.find("\t")):
        entry_rcpttocmd = entry_rcpttocmd.replace("\t", " ")
    token2 = entry_rcpttocmd[4:len(entry_rcpttocmd)-1]
    token2, token3 = token2.split(":",1)
    if token2.find(" ")==-1:
        print "500 Syntax error: command unrecognized"
        return False
    token2 = token2.replace(" ", "")
    if token2 != "TO":
        print "500 Syntax error: command unrecognized"
        return False
    if parsePath(token3):
        print "250 OK"
        return True  

s = socket.socket()         # Create a socket object
host = sys.argv[1]  # Get local machine name
port = int(sys.argv[2])                 # Reserve a port for your service.

s.connect((host, port))

greeting =  s.recv(1024).decode()
if(greeting.find("220", 0, 4) != -1):
	print "GREET CLIENT"
	s.send("HELO " + host)

ack =  s.recv(1024).decode()

if(ack.find("250", 0, 4) != -1):
	print "Do Stuff"


#then prompt user for From:, To, Subject, Message
from_cmd_is_valid = False
recipient_num = 0
while True:
    #Prompt user for From: field
	while from_cmd_is_valid is False:
		from_cmd = raw_input("From: ")
		print parseMailbox(from_cmd)
		if parseMailbox(from_cmd) == "None":
			from_cmd_is_valid is True
			mail_from_cmd = "MAIL FROM: <" + from_cmd + ">"
			s.send(mail_from_cmd)
			response = s.recv(1024)
			if response is not "250 " + extractEmail(mail_from_cmd) + " ... Sender ok":
				break #QUIT		
        else:
            print parseMailbox(from_cmd)
    #Prompt user for To: field
	to_cmd = raw_input("To: ")
	num_recipients = to_cmd.count(',')
	recipient_list = to_cmd.split(',')
	for recipient in recipient_list:
		if parseMailbox(recipient) is "None":               
			rcpt_to_cmd = "RCPT TO:" + recipient
 			s.send(rcpt_to_cmd)
			response = s.recv(1024)
			if response is not "250 " + extractEmail(mail_from_cmd) + " ... Recipient ok":
				break #QUIT	
            recipient_num+=1
        else:
            if recipient_num>0:
                break
            else:
                print parseMailbox(to_cmd)


	subject = raw_input("Subject: ")
	message = sys.stdin.readlines("Message: ")

	s.send("DATA")
	response = s.recv(1024).decode()
	if response[3:] is not "250":
		break
	s.send("From: " + extractEmail(from_cmd))
	s.send("To: " + to_cmd)
	s.send("Subject: " + subject)
	s.send(message)
	s.send(".") 
	response = s.recv(1024).decode()
	if response is not "250 ok":
		break

s.send("QUIT")

s.close                     # Close the socket when done
