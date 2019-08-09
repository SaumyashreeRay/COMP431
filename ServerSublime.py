# from socket import *
# import sys

# serverSocket = socket(AF_INET,SOCK_STREAM)
# port = sys.argv[1]                
# serverSocket.bind(('', port))        

# s.listen(5)                 
# while True:
#    connectionSocket, address = serverSocket.accept()     # Establish connection with client.
#    connectionSocket.send('220')
#    connectionSocket.close() 

import socket               # Import socket module
import sys

# This function first checks the validity of the mail from command. 
# If those tests passes, then the path of the entry is parsed and an
# error/ok message will be printed from there
def parseMailFromCmd(entry):
   if entry.find("MAIL") == -1:                #check if the substrings "MAIL" and "FROM" appear in entry
      print "500 Syntax error: command unrecognized"      #without any special/numerical characters 
      return False
   if entry.find("FROM:") == -1:
      print "500 Syntax error: command unrecognized"
      return False
   if entry.find("OM"):
      a, b = entry.split("O", 1)
      if isSpecial(a) is True:
         print "500 Syntax error: command unrecognized"
         return False
   if (entry.find("\t")):
      entry = entry.replace("\t", " ");
   m = entry[4:]
   f = entry[4:len(entry)-1]
   t2,t3 = entry.split(":",1)
   if t2.find(' ') == -1:
      if t2.find("\t") == -1:
         print "500 Syntax error: command unrecognized"
         return False
   if f.find(" ") == -1: 
      print "500 Syntax error: command unrecognized"
      return False
   if endsWithCRLF(entry) is False:
      print "501 Syntax error in parameters or arguments"
      return False

   token1, token2 = entry.split(" ", 1)        #token1 should be MAIL, token 2 should be FROM...'''
   token2, token3 = token2.split(":",1)        #now token2 should be FROM, token3 is reverse path'''
   token2 = token2.replace(" ", "")
    
   if token1 != "MAIL":
      print "500 Syntax error: command unrecognized"
      return False
   if token2 != "FROM":
      print "500 Syntax error: command unrecognized"
      return False
   if parsePath(token3) is False:
      return False
   if parsePath(token3) is True:
      print "250 OK"
      return True
   return 

def parsePath(token3): 
    if token3.find("<") == -1:
        print "501 Syntax error in parameters or arguments"
        return False
    if token3.find(">") == -1:
        print "501 Syntax error in parameters or arguments"
        return False
    mailbox,token5 = token3.split("<", 1)
    mailbox, z = token5.split(">",1)   #mailbox is mailbox
    if token3[0] != "<":
        token3 = token3.strip()        #accounting for extra valid spaces
        if token3[0] != "<":
            print "501 Syntax error in parameters or arguments"
            return False
    if parseMailbox(mailbox) is False:
        return False
    if token3[len(mailbox)+1] != ">":
        print "501 Syntax error in parameters or arguments"
        return False
    if endsWithCRLF(token3) is False:
        print "501 Syntax error in parameters or arguments"
        return False
    else:
        return True

#This function parses though the mailbox, checking if there is "@", 
#splitting it into local part and domain, and checking the validity of 
#the two
def parseMailbox(mailbox):
   if mailbox.find('@') == -1:
      print "501 Syntax error in parameters or arguments"
      return False
   localPart, domain = mailbox.split("@",1)
   domain2 = domain.strip()     #domain cannot contain spaces before and after
   if(domain2 != domain):
      print "501 Syntax error in parameters or arguments"
      return False
   if parseLocalPart(localPart) is False:
      print "501 Syntax error in parameters or arguments" 
      return False  
   if parseDomain(domain) is False:
      print "501 Syntax error in parameters or arguments"  
      return False
   else:
      return True

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

def isSpecial(s):
    return (s.find("<") != -1 or 
    s.find(">") != -1 or s.find("(") != -1 or 
    s.find(")") != -1 or s.find("[") != -1 or
    s.find("]") != -1 or s.find("\\") != -1 or 
    s.find(".") != -1 or s.find(",") != -1 or 
    s.find(";") != -1 or s.find(":") != -1 or 
    s.find("@") != -1 or s.find("'") != -1)

# This method checks the data command
def dataCmd(data):
    if data == "DATA\n":
        return True
    else:
        if(data[:4]=="DATA") and endsWithCRLF(data):
            c, d = data.split("DATA", 1)
            if isLetterDigitString(d.strip()) or isSpecial(d.strip()):
                return False
            else:
                return True
        return False

# This method strips the parameter of superfluous characters
#  that arent in the forward/reverse path
def getDomain(mail):
    begin, middle = mail.split("a", 1)
    middle, end = middle.split(">", 1)
    return middle

# Simply checks the first few chars of input to see if 
# the command is potentially out of order
def checkCommand(cmd):
   if cmd.find("\t") != -1:
      cmd = cmd.replace("\t", " ")

   if cmd[:9] == "MAIL FROM":
        return 1
   if cmd[:7] == "RCPT TO":
        return 2
   if cmd[:4] == "DATA":
        return 3
   else:
        return 0

def extractEmail(email):
    if checkCommand(email) == 1:
        email = email[5:-1]
    if checkCommand(email) == 2:
        email = email[3:-1]
    return email.strip()
# Checks to see if given parameter ends with \n
def endsWithCRLF(dat):   
    if "\n" == dat[-1] is False:
        return False
    else:
        return True

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[1])                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
   c, addr = s.accept()     # Establish connection with client.
   print 'Got connection from', addr
   greeting_220 = "220 " + host 
   c.send(greeting_220.encode())
   hello = c.recv(1024)
   if (hello.find("HELO", 0, 5) != -1):
      print "Hello!"
      c.send("250 OK")
#variables needed to parse through data sent by client
   mail_from_cmd_is_valid = False
   rcpt_to_cmd_is_valid = False
   iteration = 0
   incomingMessage = True
   fullMessage = ""
   append = False  

#  First check the mail from command
   while mail_from_cmd_is_valid == False:
      mail_from_cmd = c.recv(1024)
      print mail_from_cmd
      if mail_from_cmd == '':
         break;
      if checkCommand(mail_from_cmd)>1:
         c.send("503 Bad sequence of commands")
         continue;        
      else:
         if parseMailFromCmd(mail_from_cmd) is True:
            c.send("250 " + extractEmail(mail_from_cmd) + " ... Sender ok")
            mail_from_cmd_is_valid = True
   if mail_from_cmd == '':                                 #break if EOF
      break;

   while rcpt_to_cmd_is_valid == False:
      receiver = c.recv(1024)
      if receiver == '':
         break;
      if iteration>0: #need at least one valid recipient
         if dataCmd(receiver) is True and checkCommand(receiver)==3:
            c.send("354 Start mail input; end with <CRLF>.<CRLF>")
            rcpt_to_cmd_is_valid = True
            break; 
      # exit receiver loop only when valid DATA command entered
      #check for out of order commanding
      if (checkCommand(receiver) == 1): 
         c.send("503 Bad sequence of commands")
      elif dataCmd(receiver) is True: #more thorough than the next data check
         c.send("503 Bad sequence of commands")
      elif checkCommand(receiver) == 3:
         c.send("500 Syntax error: command unrecognized")
      else:
         if parseRcptToCmd(receiver) is True:
            recipients.append(receiver.rstrip("\n"))
            iteration+=1 
   if receiver == '':
      break;

   #lastly check the message         
   while incomingMessage == True:
      dataMessage = c.recv(1024)
      if dataMessage == '':
         break;
      if dataMessage[8:] == "Subject:":
         dataMessage = dataMessage + "\n"
      if dataMessage == ".\n":
         c.send("250 OK")
         append = True
         incomingMessage = False
         break
      fullMessage = fullMessage + dataMessage 
   if dataMessage == '':
      break;

   #now print it into a file
   if append is True:
      for r in recipients:
         rString = getDomain(r)
         f = open('forward/%s' %rString,"a+") 
         f.write(fullMessage)          
         f.close()

   c.close()                # Close the connection

