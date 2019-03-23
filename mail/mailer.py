import email
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:

    is_authenticated = False

    def __init__(self, smtp_server, smtp_port):
        context = ssl.create_default_context()
        self.mail_server = smtplib.SMTP_SSL(
            host=smtp_server, port=smtp_port, context=context)

    def authenticate(self, username, password):
        self.mail_server.login(username, password)
        self.is_authenticated = True

    def send_mail(self, subject, sender, recipients, body, attachments, inline_images):

        if not self.is_authenticated:
            raise Exception('Please authenticate before sending mail')

        message = MIMEMultipart()

        message['From'] = '{} <{}>'.format(sender['name'], sender['email'])
        message['To'] = ' '.join(recipients['To'])
        message['Cc'] = ' '.join(recipients['Cc'])
        message['Bcc'] = ' '.join(recipients['Bcc'])
        message['Subject'] = subject

        message.attach(MIMEText(body, "html"))

        for attachment in attachments:
            with open(attachment['path'], "rb") as file:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment; filename= {}".format(attachment['name'])
            )
            message.attach(part)

        for image in inline_images:
            with open(image['path'], 'rb') as file:
                msg_image = MIMEImage(file.read(), name=image['name'])
            msg_image.add_header('Content-ID', '<{}>'.format(image['cid']))
            message.attach(msg_image)

        mail_message = message.as_string()
        self.mail_server.sendmail(sender['email'], list(
            set(recipients['To'] + recipients['Cc'] + recipients['Bcc'])), mail_message)
