import os
import smtplib
import ssl
from typing import List

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders

from config import USERNAME, RECEIVER_EMAIL, SENDER_EMAIL, SENDER_EMAIL_PASS
from pokemon import Pokemon
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))


PORT = 465


def send_notification(pokemon: Pokemon,
                      n_attempts: int,
                      shiny_found: bool,
                      to_email: str = RECEIVER_EMAIL,
                      from_email: str = SENDER_EMAIL,
                      from_pass: str = SENDER_EMAIL_PASS,
                      username: str = USERNAME,
                      attachments: List[str] = [],
                      send: bool = True):
    """Sends a notification to the specified email to provide update
    on shiny hunting status. By default, uses the configuration file
    to determine emails, sender password and username."""
    logger.info(f"drafting email to notify user {username}")
    
    # establishes the message to fill in each requirement of the email
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    if shiny_found:
        subject = f"FOUND Shiny {pokemon.name}!"
    else:
        subject = f"Shiny Hunting Status For {pokemon.name}"
    message["Subject"] = subject

    # standard message given html formatting
    if shiny_found:
        p1 = "I hope you're sitting down, because the news of a lifetime is coming upon you."
        p2 = f"Thanks in no small part to the ingenuity of our development team, we have been able to afford the luxury of carefree\
            shiny hunting. Upon arrival to your gaming system, you will find the battle in progress of a shiny <b>{pokemon.name}</b>! Take great care\
            to catch the beast as there are no assurances of another one arriving anytime soon."
        paragraph = f"{p1}<br>{p2}"
    else:
        paragraph = f"Unfortunately, no shiny <b>{pokemon.name}</b> has been found yet.\
            Rest assured, hunting will continue until a shiny is found!"
    html = f"""
    <html>
        <body>
            Hi {username},
            <br>
            <p>{paragraph}</p>
            <p>Number of attempts: {n_attempts}</p>
            <br>
            Regards,
            <br>
            Shiny Hunting Team
            <br><br>
        </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))
    attachments.append(pokemon.get_shiny_img_fn())
    attachments = list(set(attachments))  # only unique files
    for file in attachments:
        with open(file, "rb") as attached_file:
            attachment = MIMEBase("application", "octet-stream")
            attachment.set_payload(attached_file.read())

        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", f"attachment; filename={os.path.basename(file)}")
        message.attach(attachment)

    context = ssl.create_default_context()
    logger.debug(f"email message: {message.as_string()}")
    if send:
        with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
            server.login(from_email, from_pass)
            server.sendmail(from_email, to_email, message.as_string())
            logger.info("Email successfully sent")
    else:
        logger.info("Message ready for sending")
