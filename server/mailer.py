import os
import smtplib
import socket
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from generic_processor import GenericProcessor

mailer_server = 'localhost'
from_address= 'hemanth@colorado.edu'

def successfull_request_sumission(cc_emails):
    to_email_list = 'hemanth@colorado.edu'
    cc_email_list = []
    bcc_email_list = []
    recipients = to_email_list + cc_email_list + bcc_email_list
    msg = MIMEMultipart()
    msg["From"] = from_address
    msg["To"] = ", ".join(to_email_list)
    msg["Cc"] = ", ".join(cc_email_list)
    msg["Bcc"] = ", ".join(bcc_email_list)
    msg["Subject"] = "payment request successfully placed"
    html_content = """
<p>Hello,</p>
<p>Your payment request has been successfully submitted.</p>
"""
    body = GenericProcessor.html_template_returner(html_content)
    msg.attach(MIMEText(body, "html"))
    s = smtplib.SMTP(mailer_server)
    s.sendmail(from_address, recipients, msg.as_string())
    s.quit()