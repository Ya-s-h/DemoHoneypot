# Author: Yash Aggarwal



# Importing Modules
import asyncore
import time
from smtpd import SMTPServer
import re


def FormatTime():
    """
    
    For Generating time in a pre-defined format (YYYYMMDD-HHMMSS)
    """

    return '%04d%02d%02d-%02d%02d%02d' % time.localtime()[0:6]


class logFile():
    """
    
    A class object to create and write in a log file
    
    """
    def __init__(self, filename=f"smtp-honeypot-{FormatTime()}.log"):
        """
        filename, by default is smtp-honeypot-time.log
        can be changed by changing value of filename at time of obj creation
        """
        self.filename = filename
        self.f = open(self.filename, 'w')
    
    def Write(self, line):
        """
        To only write the content in the file
        """
        if self.f:
            try:
                self.f.write(line + "\n")
                self.f.flush()
            except:
                pass

    def WriteWithTimeStamped(self, line):
        """
        To write in file but with time stamps
        *More preferred*
        """
        self.Write(f"{FormatTime()}: {line}")

    def Close(self):
        """
        Close file
        """
        if self.f:
            self.f.close()
            self.f = None

class Server(SMTPServer):
    """
    Creates an object for SMTP Server
    """
    def process_message(self, peer, mailfrom, rcpttos, data):
        """
        Processing message for writting in logfile
        """
        global Output

        subject = ''
        oMatch = re.search('\nSubject: ([^\n]+)\n', data)
        if oMatch != None:
            subject = repr(oMatch.groups()[0])

        # Logging
        Output.LineTimestamped('Email: %s %s %s %s' % (repr(peer), repr(mailfrom), repr(rcpttos), subject))

        # Fetching mail content from the data
        f = open('%s-%s.eml' % (FormatTime(), ''.join([c for c in subject.replace(' ', '_') if c.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789_'])), 'wb')
        f.write(data.encode())
        f.close()


def SMTPHoneypot(ports=dict(), IPaddress = 'localhost'):
    """
    Creating a Honeypot server with localhost as default IP address
    """
    global Output

    Output = logFile()
    for port in ports.values():
        server = Server((IPaddress, port), None, decode_data=True)
        Output.WriteWithTimeStamped(f"Started Listening at {IPaddress} : {port}")
    asyncore.loop()


def main():
    """
    Equivalent to int main() function of C/C++
    Kind of ‾\_('‿')_/‾
    """
    # protocol = input("Choose Protocol (HTTP/SSH/FTP)\nEnter: ")
    # List of ports for SSH, HTTP and FTP protocol
    ports = {
        "SSH" : 22,
        "HTTP" : 80,
        "FTP" : 21,
        "SMTP" : 25
    }
    SMTPHoneypot(ports=ports)
    # if protocol.upper() not in ports:
    #     print("Invalid Protocol.\nRunning in SMTP Mode(By Default)")
    #     SMTPHoneypot()
    # else: 
    #     SMTPHoneypot(port=ports[protocol.upper()])

if __name__ == "__main__":
    main()
