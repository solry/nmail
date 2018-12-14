import os
import smtplib
import traceback
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

try:
    import yaml
    import_yaml = True
except (ModuleNotFoundError, ImportError):
    print('yaml module has not been imported. '
          'config.yml file will not be read')
    import_yaml = False

COMMASPACE = ', '

class AttachmentError(Exception):
    pass

class ConfigurationError(Exception):
    pass

def send_mail(to=(), cc=None, bcc=None,
              subject='No subject',
              text='No Text',
              attachments=(),
              send_as=None,
              smtp_server=None, smtp_port=None,
              login=None, password=None,
              config_file='default'):


    #  Configuration:
    if import_yaml:
        if config_file == 'default':
            # Get default config file from package folder:
            config_file = os.path.dirname(os.path.abspath(__file__)) + '/config.yml'

        config = __read_config(config_file)
        print(config)
        smtp_server, smtp_port, login, password = __update_config(smtp_server, smtp_port, login, password, config)

    __verify_config(smtp_server, smtp_port, login, password)

    #  Message construction:
    mesg = MIMEMultipart()
    mesg['Subject'] = subject
    if send_as:
        mesg['From'] = send_as
    else:
        mesg['From'] = login


    recipients = []
    if to:
        mesg['To'] = COMMASPACE.join(to)
        recipients.extend(list(to))
    if cc:
        mesg['Cc'] = COMMASPACE.join(cc)
        recipients.extend(list(cc))
    if bcc:
        mesg['Bcc'] = COMMASPACE.join(bcc)
        recipients.extend(list(bcc))

    mesg.preamble = '\n'
    __attach(mesg, attachments)
    mesg.attach(MIMEText(text, 'plain'))
    composed = mesg.as_string()
    # Send the email
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(login, password)
            s.sendmail(mesg['From'], recipients, composed)
            s.close()

        return True

    except:
        traceback.print_exc()
        return False


def __attach(mesg, attachments):
    """
    :param mesg: MIME-Multipart message
    :param attachments:  List of attachments
    :return:
    """
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', 'octet-stream')
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            mesg.attach(msg)
        except:
            traceback.print_exc()
            raise AttachmentError(f'Unable to attach file: {file}')


def __read_config(config_file):
    """
    Read config from yaml file
    :param config_file:
    :return:
    """
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def __update_config(smtp_server, smtp_port, login, password, config):
    """
    Update configuration variables
    :param smtp_server:
    :param smtp_port:
    :param login:
    :param password:
    :param config:
    :return:
    """
    if smtp_server is None:
        smtp_server = config.get('smtp_server')
    if smtp_port is None:
        smtp_port = config.get('smtp_port')
    if login is None:
        login = config.get('login')
    if password is None:
        password = config.get('password')
    return smtp_server, smtp_port, login, password


def __verify_config(smtp_server, smtp_port, login, password):
    WARNING_MESSAGE = '{} configured impoperly.\n' \
                      'Expected type: {}\n'\
                      'Configured value: {}'
    if type(smtp_server) != str:
        raise ConfigurationError(WARNING_MESSAGE.format('smtp_server', 'str', smtp_server))
    if type(smtp_port) != int:
        raise ConfigurationError(WARNING_MESSAGE.format('smtp_port', 'int', smtp_port))
    if type(login) != str:
        raise ConfigurationError(WARNING_MESSAGE.format('login', 'str', login))
    if type(password) != str:
        raise ConfigurationError(WARNING_MESSAGE.format('password', 'str', password))