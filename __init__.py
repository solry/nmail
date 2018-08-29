import os
import smtplib
import traceback
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def send_mail(to=(), cc=(),
              subject='No subject',
              text='No Text',
              attachments=(),
              send_as=None,
              detail_answer=False,
              smtp_server=None, smtp_port=587,
              login=None, password=None):


    outer = MIMEMultipart()
    outer['Subject'] = subject
    if send_as:
        outer['From'] = send_as
    else:
        outer['From'] = login

    outer['To'] = COMMASPACE.join(to)
    if cc:
        outer['Cc'] = COMMASPACE.join(cc)

    outer.preamble = '\n'

    recipients = to + cc

    __attach(outer, attachments)
    outer.attach(MIMEText(text, 'plain'))
    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(login, password)
            s.sendmail(send_as, recipients, composed)
            s.close()

        return True

    except:
        traceback.print_exc()
        return False

def __attach(outer, attachments):
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', 'octet-stream')
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            traceback.print_exc()
            raise AttachmentError(f'Unable to attach file: {file}')

class AttachmentError(Exception):
    pass