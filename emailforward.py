import imaplib
import smtplib
import email.utils
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.parser import BytesParser
from email.policy import default

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('tsesiren@gmail.com', 'ddhc plrd cmtf sfkm')
mail.select('"[Gmail]/All Mail"')

status, email_ids = mail.search(None, '(FROM "Rightmove Property Alerts")')
emails = []

for email_id in email_ids[0].split():
    status, data = mail.fetch(email_id, '(RFC822)')
    raw_email = data[0][1]
    email_message = BytesParser(policy=default).parsebytes(raw_email)

    body = ""
    for part in email_message.walk():
        if part.get_content_type() == "text/html":
            body += part.get_payload(decode=True).decode()

    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        email_date =email.utils.mktime_tz(date_tuple)
        emails.append((email_date, body))
    
if emails:
    most_recent_email = max(emails, key=lambda x:x[0])[1] 

if most_recent_email:
    msg = MIMEMultipart("alternative")
    sender = 'tsesiren@gmail.com'
    recipients = ['chukwong2000@yahoo.com.hk, teresamlso@gmail.com']
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = "New property alerts for " + str(date.today())
    msg.attach(MIMEText(most_recent_email, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('tsesiren@gmail.com', 'ddhc plrd cmtf sfkm')
    server.sendmail(sender, recipients, msg.as_string())
    server.quit()

