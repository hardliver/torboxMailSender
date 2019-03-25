import socket
import socks
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
import json


class SocksSMTP(SMTP):

    def __init__(self,
            host='',
            port=0,
            local_hostname=None,
            timeout=socket._GLOBAL_DEFAULT_TIMEOUT,
            source_address=None,
            proxy_type=None,
            proxy_addr=None,
            proxy_port=None,
            proxy_rdns=True,
            proxy_username=None,
            proxy_password=None,
            socket_options=None):

        self.proxy_type=proxy_type
        self.proxy_addr=proxy_addr
        self.proxy_port=proxy_port
        self.proxy_rdns=proxy_rdns
        self.proxy_username=proxy_username
        self.proxy_password=proxy_password
        self.socket_options=socket_options
        # if proxy_type is provided then change the socket to socksocket
        # behave like a normal SMTP class.
        if self.proxy_type:
            self._get_socket = self.socks_get_socket

        super(SocksSMTP, self).__init__(host, port, local_hostname, timeout, source_address)

    def socks_get_socket(self, host, port, timeout):
        if self.debuglevel>0:
            self._print_debug('connect: to', (host, port), self.source_address)
        return socks.create_connection((host, port),
                timeout=timeout,
                source_address=self.source_address,
                proxy_type=self.proxy_type,
                proxy_addr=self.proxy_addr,
                proxy_port=self.proxy_port,
                proxy_rdns=self.proxy_rdns,
                proxy_username=self.proxy_username,
                proxy_password=self.proxy_password,
                socket_options=self.socket_options)

with open('key.json') as f:
    k = json.load(f)
    username = k['username']
    password = k['password']

_SMTP = SocksSMTP(
    host="torbox3uiot6wchz.onion",
    port=25,
    proxy_type=socks.SOCKS5,
    proxy_addr="127.0.0.1",
    proxy_port=9050
)
# _SMTP.ehlo()
# _SMTP.starttls()
_SMTP.login('{}@torbox3uiot6wchz.onion'.format(username), password)


def getMailScript(subject=None, sender=None, to=None, text=None):
    if not sender:
        sender = 'Mail bot'
    message            = MIMEText(text)
    message['Subject'] = Header(subject)
    message['From']    = Header(sender)
    if to:
        message['To'] = Header(to)
    print(message.as_string())
    return message


if __name__ == "__main__":
    msg = {
        'subject': 'Test send mail',
        'text'   : """\
Test send mail via python.
https://www.python.org
"""
    }
    message = getMailScript(**msg)
    # print(message)

    smtp = _SMTP
    smtp.sendmail('username@torbox3uiot6wchz.onion', ['username@torbox3uiot6wchz.onion'], message.as_string())
