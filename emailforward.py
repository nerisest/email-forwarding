#!/usr/bin/env python3

import imaplib
import smtplib
import email.utils
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import BytesParser
from email.policy import default

# by using IMAP, emails can be retrieved from different email clients
# using an email address and app password, mails can be retrieved by specifiying an inbox
mail = imaplib.IMAP4_SSL('IMAP_SERVER')
mail.login('EMAIL_ADDRESS', 'PASSWORD')
mail.select('"SPECIFIC_INBOX"')

# for information criteria search, the documentation can be found here at https://datatracker.ietf.org/doc/html/rfc3501#section-6.4.4
status, email_ids = mail.search(None, '(YOUR_SEARCH_CRITERIA)')
emails = []

for email_id in email_ids[0].split():
    # fetch the email with the given query, and parse the data with "data[0][1]"
    # [0] represents the unique identifier, [1] represents the actual data in bytes format
    status, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = BytesParser(policy=default).parsebytes(raw_email)    # "policy=default" uses the standard formatting '\n'

    # decoding the Message object from the email message and storing in body
    body = ""
    for part in email_message.walk():
        if part.get_content_type() == "text/html":
            body += part.get_payload(decode=True).decode()             

    # lists out the dates sent for each emails matching the subject
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        email_date = email.utils.mktime_tz(date_tuple)
        emails.append((email_date, body))
    
 # returns the most recent email by filtering out the list of emails
if emails:
    most_recent_email = max(emails, key=lambda x:x[0])[1] 

# if a most recent email is found, create a MIMEMultipart object for preparation of sending messages
# start up a SMTP server to connect to Gmail and send the email with the provided recipients
if most_recent_email:
    msg = MIMEMultipart("alternative")
    sender = 'EMAIL_ADDRESS'
    recipients = ['RECIPIENT1, RECIPIENT2']
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "New property alerts for " + str(date.today())
    msg.attach(MIMEText(most_recent_email, 'html'))

    server = smtplib.SMTP('SMTP_SERVER', 587)
    server.starttls()
    server.login('EMAIL_ADDRESS', 'PASSWORD')
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

