import email, smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465

sender_email = "pokepy155@gmail.com"
password = "iieszmlurcusscoa"

name = "Tyranitar"
receiver_email = "treysauce03@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = """
    Subject: Hi there
    
    This message is sent from Python."""

html = f"""
<html>
    <body>
        <p>Hi {name},<br>
            How are you?<br>
        <p>
    <body>
<html>
"""

part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

message.attach(part1)
message.attach(part2)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())