import os, smtplib, ssl

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

DOCUMENT = os.path.join('images', 'test_images', 'battle_img_1.png')
NAME = "Tyranitar"
POKEMON = "Gyarados"
PORT = 465
SENDER_EMAIL = "pokepy155@gmail.com"
PASSWORD = "iieszmlurcusscoa"

def send_notification(receiver_email: str):
    '''sends emails to the account of your choice if and when the system locates a shiny'''
    #Establishes the message to fill in each requirement of the email
    message = MIMEMultipart()
    message["Subject"] = "A Shiny Has Been FOUND!"
    message["From"] = SENDER_EMAIL
    message["To"] = receiver_email

    #standard message given html formatting
    html = f"""
    <html>
        <body>
            <p>Hi {NAME},<br>
                I hope you're sitting down, because the news of a lifetime is coming upon you.<br>
            </p>
            <p>
                Thanks in no small part to the ingenuity of our development team, we have been able to afford the luxury of carefree
                shiny hunting. Upon arrival to your gaming system, you will find the battle in progress of a shiny <b>{POKEMON}</b>! Take great care
                to catch the beast as there are no assurances of another one arriving anytime soon.
            </p>
        </body>
    </html>
    """

    part = MIMEText(html, "html")

    message.attach(part)

    with open(DOCUMENT, "rb") as attachment:
        file = MIMEBase("application", "octet-stream")
        file.set_payload(attachment.read())

    encoders.encode_base64(file)

    file.add_header("Content-Disposition", f"attachment; filename= {DOCUMENT}")

    message.attach(file)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())

if __name__ == "__main__":
    receiver_email = "treysauce03@gmail.com"
    send_notification(receiver_email)