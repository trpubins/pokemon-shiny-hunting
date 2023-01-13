import email, smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

NAME = "Tyranitar"
POKEMON = "Gyarados"
port = 465

sender_email = "pokepy155@gmail.com"
password = "iieszmlurcusscoa"

receiver_email = "treysauce03@gmail.com"

message = MIMEMultipart("alternative")
message["Subject"] = "A Shiny Has Been FOUND!"
message["From"] = sender_email
message["To"] = receiver_email

html = f"""
<html>
    <body>
        <p>Hi {NAME},<br>
            I hope you're sitting down, because the news of a lifetime is coming upon you.<br>
        <p>
        <p>
            Thanks in no small part to the ingenuity of our development team, we have been able to afford the luxury of carefree
            shiny hunting. Upon arrival to your gaming system, you will find the battle in progress of a shiny {POKEMON}! Take great care
            to catch the beast as there are no assurances of another one arriving anytime soon.
        <p>
    <body>
<html>
"""

part = MIMEText(html, "html")

message.attach(part)

context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())