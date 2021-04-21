import smtplib
from smtplib import SMTPException

def email_update(subject, content, sender, recipient, server):

    receivers = [recipient]
    message = """From: {}
To: {}
Subject: {}

{}
""".format(sender, recipient, subject, content)
    try:
        smtpObj = smtplib.SMTP(server)
        smtpObj.sendmail(sender, receivers, message)
        print("Sent update email")
    except SMTPException:
        print("Failed to send update email")