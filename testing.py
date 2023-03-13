
import threading
import smtpd
import asyncore
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()


def send_email(user, pwd, recipient, body, subject=None):


    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        client = smtplib.SMTP("smtp.gmail.com", 587)
        client.ehlo()
        client.starttls()
        client.login(gmail_user, gmail_pwd)
        client.sendmail(FROM, TO, message)
        client.close()
        print ('successfully sent the mail')
    except Exception as e:
        print (e)



# port should match your SMTP server
client = smtplib.SMTP("localhost", port=25)

fromaddr = "aggarwalyash22623@gmail.com"
toaddrs = "vasu2013agg@gmail.com"
msg = 'Hello'

send_email(user =fromaddr, pwd = os.environ['pass'], recipient= toaddrs, body= msg)
client.quit()