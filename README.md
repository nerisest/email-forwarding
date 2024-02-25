# email-forwarding

a small little automation script that I thought of over the weekend. main functionality is to forward the most recent price alert updates (email) regarding rents in the City of Edinburgh.

a little run-through of how it works:
- script logs in to the Gmail IMAP server with my email address and app password, then selects the correct mailbox
- the script then searches through my mailbox, looking for emails sent from "Rightmove Property Alerts"
- the script then fetches those queried emails and parses them using ByteParser
  - as the original email is in HTML format, we will first check if the content type is correct before appending       it to the forwarding body
- to find the most recent email, the script stores the dates sent into a tuple, then extracts the one with the most recent date
  - this email is then passed into a MIMEMultiPart object, creating the email with respective senders and recipients
- the script sets up a SMTP server, connects to Gmail, establishes a TLS connection and sends the email before closing the connection

**my command for crontab does not work properly so the script is manually executed when a new mail is received. will be fixed in a later date.**

~~the script is currently running every day at midnight UTC (to facilitate my parents, where they are currently situated in UTC+8 timezone) through **crontab**, with the following commands:~~
~~- 0 0 * * * /home/tsesiren/Desktop/other stuff/email-automation-thing/emailforward.py~~
