# -*- coding: utf-8 -*-

from smtplib import SMTPException

import pytest
from mock import patch, call
from nameko import config

from users.dependencies.email import EmailDependency
from users.exceptions import EmailSendError


class TestEmailDependency:

    @config.patch({
        "MAIL_HOST": "163.com",
        "EMAIL_USER": "email_user",
        "EMAIL_PASSWORD": "email_password",
        "EMAIL_SENDER": "email_sender",
    })
    def test_email_get_dependency(self, mock_container):
        dependency_provider = EmailDependency().bind(mock_container, "email")

        worker_ctx = None

        with patch("users.dependencies.email.smtplib"):
            email = dependency_provider.get_dependency(worker_ctx)

        assert isinstance(email, EmailDependency.EmailBase)

    @config.patch({
        "MAIL_HOST": "163.com",
        "EMAIL_USER": "email_user",
        "EMAIL_PASSWORD": "email_password",
        "EMAIL_SENDER": "email_sender",
    })
    def test_email_dependency_send_email(self, mock_container):
        dependency_provider = EmailDependency().bind(mock_container, "email")

        worker_ctx = None

        with patch("users.dependencies.email.smtplib"):
            email = dependency_provider.get_dependency(worker_ctx)

            email.send("email_receiver", "email_subject", "email_content")

        assert email.smtp_obj.sendmail.call_args == call(
            "email_sender", ["email_receiver"],
            'Content-Type: text/plain; charset="us-ascii"\n'
            'MIME-Version: 1.0\n'
            'Content-Transfer-Encoding: 7bit\n'
            'From: email_sender\n'
            'Subject: email_subject\n'
            'To: email_receiver\n'
            '\nemail_content'
        )

    @config.patch({
        "MAIL_HOST": "163.com",
        "EMAIL_USER": "email_user",
        "EMAIL_PASSWORD": "email_password",
        "EMAIL_SENDER": "email_sender",
    })
    def test_email_dependency_send_email_raise_error(self, mock_container):
        dependency_provider = EmailDependency().bind(mock_container, "email")

        worker_ctx = None

        with patch("users.dependencies.email.smtplib"):
            email = dependency_provider.get_dependency(worker_ctx)
            email.smtp_obj.sendmail.side_effect = SMTPException()

            with pytest.raises(EmailSendError):
                email.send("email_receiver", "email_subject", "email_content")
