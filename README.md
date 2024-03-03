# email-forwarding

## Date: 21st Februrary, 2024

### Introduction

A small automation script that I thought of over the weekend. The main functionality is to forward the **most recent email**, given a specific inbox and a search criteria (sender/subject...).<br>
This was used to forward the most recent price alerts regarding properties for rent in the City of Edinburgh, for my usage. However, it can be applied to other uses.

a little run-through of how it works:
- script logs in to the Gmail IMAP server with my email address and app password, then selects the correct mailbox
- the script then searches through my mailbox, looking for emails sent from "Rightmove Property Alerts"
- the script then fetches those queried emails and parses them using ByteParser
  - as the original email is in HTML format, we will first check if the content type is correct before appending       it to the forwarding body
- to find the most recent email, the script stores the dates sent into a tuple, then extracts the one with the most recent date
  - this email is then passed into a MIMEMultiPart object, creating the email with respective senders and recipients
- the script sets up a SMTP server, connects to Gmail, establishes a TLS connection and sends the email before closing the connection

### Setup
General information: **An app password is required for the IMAP/SMTP servers to work with the script.** Procedures can be found at the links below for different email clients:
- [Outlook](https://support.microsoft.com/en-gb/account-billing/using-app-passwords-with-apps-that-don-t-support-two-step-verification-5896ed9b-4263-e681-128a-a6f2979a7944)
- [Gmail](https://support.google.com/accounts/answer/185833?hl=en)
- [Yahoo](https://help.yahoo.com/kb/SLN15241.html)
- [Apple Mail](https://support.apple.com/en-gb/102654)

w/o automation: 
- Download the script and fill in the fields with the format "UPPERCASE_WITH_UNDERSCORES"
- 
