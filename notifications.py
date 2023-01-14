import os, smtplib, ssl

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from pokemon import Pokemon

from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from config import USERNAME, RECEIVER_EMAIL, SENDER_EMAIL, PASSWORD
port = 465


def send_notification(receiver_email: str, pokemon: Pokemon, send: bool=True):
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
            <p>Hi {USERNAME},<br>
                I hope you're sitting down, because the news of a lifetime is coming upon you.<br>
            </p>
            <p>
                Thanks in no small part to the ingenuity of our development team, we have been able to afford the luxury of carefree
                shiny hunting. Upon arrival to your gaming system, you will find the battle in progress of a shiny <b>{pokemon.name}</b>! Take great care
                to catch the beast as there are no assurances of another one arriving anytime soon.
            </p>
        </body>
    </html>
    """

    part = MIMEText(html, "html")

    message.attach(part)

    with open(pokemon.get_shiny_img_fn(), "rb") as attachment:
        file = MIMEBase("application", "octet-stream")
        file.set_payload(attachment.read())

    encoders.encode_base64(file)

    file.add_header("Content-Disposition", f"attachment; filename= {pokemon.get_shiny_img_fn()}")

    message.attach(file)

    context = ssl.create_default_context()
    if send:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
            logger.info("Email successfully sent")
    else:
        logger.info("Message ready for sending")

if __name__ == "__main__":
    # document = os.path.join('tests','test_files','test_images', 'battle_img_1.png')
    pokemon = Pokemon("Gyarados")

    send_notification(RECEIVER_EMAIL, pokemon, send=True)