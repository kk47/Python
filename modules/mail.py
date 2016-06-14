#!/usr/bin/env python

import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
    assert type(send_to)==list
    assert type(files)==list
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach(MIMEText(text))

    for f in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
        msg.attach(part)
    smtp = smtplib.SMTP(server)
    smtp.set_debuglevel(True)
    smtp.login("alert@aggstor.com", "warn123")
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__ == "__main__":
    sfrom = "alert@aggstor.com"
    sto = ["kuangkai@aggstor.com"]
    subject = "This is a test of attach"
    text = "This is body"
    files = ["/tmp/dayuwinsrv_2015-11-19_04-02-32.dmp"]
    server = "smtp.exmail.qq.com"

    send_mail(sfrom, sto, subject, text, files, server)

    
