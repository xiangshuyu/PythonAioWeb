#!/usr/bin/python
# -*- coding: utf-8 -*-

import mimetypes
import os
import smtplib
import sys
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from optparse import OptionParser

from util.logger.logger import Logger

logger = Logger(__name__)

COMMASPACE = ', '


class Email(object):
    __slots__ = '_sender', '_recipients', '_subject', '_content', '_attachment', '_output', '_host'

    def __init__(self, sender: tuple,
                 recipients: list, subject: str = 'send by python', content=None,
                 attachment: list = list(), output: str = '',
                 host: tuple = ('127.0.0.1', 25)):
        """
        :param sender:  发送人 （邮箱账号, 授权密码）
        :param recipients:  接收方, 可填多个 [1, 2, 3]
        :param subject:  主题
        :param content:  文本内容
        :param attachment:  附件所在目录
        :param host:  smtp服务器地址和端口 (地址, 端口)
        """
        self._sender = sender
        self._recipients = recipients
        self._subject = subject
        self._attachment = attachment
        self._output = output
        self._host = host

        if not content:
            self._content = list()
        elif isinstance(content, str):
            self._content = [(content, 'p')]
        elif isinstance(content, list):
            self._content = content

    @property
    def host(self):
        return self._host

    @property
    def sender(self):
        return self._sender

    @property
    def recipients(self):
        return self._recipients

    @property
    def subject(self):
        return self._subject

    @property
    def content(self):
        return self._content

    @property
    def attachment(self):
        return self._attachment

    @property
    def output(self):
        return self._output

    def __iter__(self):
        return iter([self.__getattribute__(x) for x in self.__slots__])


def send_email(email: Email):
    senderTuple, recipients, subject, content, attachment, output, hostInfo = email
    (sender, password) = senderTuple
    (host, port) = hostInfo
    if not sender or not recipients or not host:
        raise AttributeError('the sender, recipients, server must not be null')

    mime = MIMEMultipart()
    mime['Subject'] = subject
    mime['To'] = COMMASPACE.join(recipients)
    mime['From'] = sender

    _wrap_content(content=content, mime=mime)

    for directory in attachment:
        _wrap_attachment(directory=directory, mime=mime)

    composed = mime.as_string()

    if output:
        fp = open(output, 'w')
        fp.write(composed)
        fp.close()
    else:
        s = smtplib.SMTP(host=host, port=port)
        s.starttls()
        s.set_debuglevel(1)
        s.login(user=sender, password=password)
        s.sendmail(sender, recipients, composed)
        s.quit()


def _wrap_content(content: list, mime: MIMEMultipart):
    if not content:
        return MIMEText('', _subtype='plain', _charset='utf-8')
    messageBody = ''
    for c in content:
        if isinstance(c, tuple):
            c_text, c_type = c
            if c_type == 'p':
                messageBody += '<p>%s</p>' % c_text
            if c_type == 'img':
                messageBody += '<p><img src="%s"></p>' % c_text
        elif isinstance(c, str):
            messageBody += '<p>%s</p>' % c
        else:
            logger.warn('the content item should be a "str" or "tuple", but is a "%s"' % type(c))
            continue

    message = '<html><body>%s</body></html>' % messageBody

    msg = MIMEText(message, _subtype='html', _charset='utf-8')
    mime.attach(msg)


def _wrap_attachment(directory: str, mime: MIMEMultipart):
    if not os.path.isdir(directory):
        return

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue

        c_type, encoding = mimetypes.guess_type(path)
        if c_type is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            c_type = 'application/octet-stream'

        maintype, subtype = c_type.split('/', 1)
        print('type: %s name: %s' % (maintype, filename))
        if maintype == 'text':
            fp = open(path)
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(path, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(path, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(path, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(msg)

        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.add_header('Content-ID', '<0>')
        msg.add_header('X-Attachment-Id', '0')
        mime.attach(msg)


def main():
    parser = OptionParser(usage="""
    Send the contents of a directory as a MIME message.

    Usage: %prog [options]

    Unless the -o option is given, the email is sent by forwarding to your local
    SMTP server, which then does the normal delivery process.  Your local machine
    must be running an SMTP server.
    """)

    parser.add_option('-d', '--directory', type='string', action='store')
    parser.add_option('-o', '--output', type='string', action='store', metavar='FILE')
    parser.add_option('-s', '--sender', type='string', action='store', metavar='SENDER')
    parser.add_option('-p', '--password', type='string', action='store', metavar='SENDER PASSWORD')
    parser.add_option('-r', '--recipients', type='string', action='append', metavar='RECIPIENT')
    parser.add_option('-h', '--host', type='string', action='append', metavar='SMTP HOST')
    parser.add_option('-c', '--content', type='string', action='append', metavar='CONTENT')

    opts, args = parser.parse_args()
    if not opts.sender or not opts.recipients:
        parser.print_help()
        sys.exit(1)

    directory = opts.directory
    if not directory:
        directory = '.'

    send_email(Email(sender=(opts.sender, opts.password), recipients=opts.recipients,
                     attachment=[directory], content=opts.content, host=opts.host))


if __name__ == '__main__':
    e = Email(sender=('15200822495@163.com', 'xsy8513692'), recipients=['663548922@qq.com'], subject='python邮件发送',
              attachment=['/home/xsy/temp/dir'], content=['this is a test', ('cid:0', 'img')], host=('smtp.163.com', 25))
    send_email(e)
