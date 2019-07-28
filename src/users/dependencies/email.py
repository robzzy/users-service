# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTPException

from nameko import config
from nameko.extensions import DependencyProvider

from users.exceptions import EmailSendError


class EmailDependency(DependencyProvider):

    class EmailBase:

        def __init__(self, config):
            self.config = config
            self.smtp_obj = smtplib.SMTP()
            self.mail_host = config["MAIL_HOST"]
            self.user = config["EMAIL_USER"]
            self.password = config["EMAIL_PASSWORD"]
            self.sender = config["EMAIL_SENDER"]

            self._login()

        def _login(self):
            self.smtp_obj.connect(self.mail_host, 25)
            self.smtp_obj.login(
                self.user, self.password
            )

        def send(self, receiver, subject, content):

            receivers = [receiver]
            Messager = MIMEText(content)

            Messager["From"] = Header(self.sender)
            Messager["Subject"] = Header(subject)
            Messager["To"] = Header(receiver)

            try:
                self.smtp_obj.sendmail(
                    self.sender, receivers, Messager.as_string()
                )
            except SMTPException:
                raise EmailSendError(f"Failed to send email to {receiver}")

    def get_dependency(self, worker_ctx):
        return EmailDependency.EmailBase(config)
