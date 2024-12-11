"""  Test send mail
"""

from unittest.mock import patch

from django.core import mail
from django.test import TestCase

from core_main_app.utils.notifications.mail import (
    send_mail_to_website_contacts,
)


class TestSendEmailToWebsiteContacts(TestCase):
    """TestSendEmailToWebsiteContacts"""

    def test_send_mail_to_website_contact(
        self,
    ):
        """test_send_mail_to_website_contact"""

        # Act
        send_mail_to_website_contacts(
            subject="test", path_to_template="mail.html"
        )

        # Assert
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[Test]test")
        self.assertEqual(
            mail.outbox[0].to, ["john@example.com", "mary@example.com"]
        )

    def test_send_mail_to_website_contact_with_context(
        self,
    ):
        """test_send_mail_to_website_contact_with_context"""

        # Act
        send_mail_to_website_contacts(
            subject="test",
            path_to_template="mail.html",
            context={"username": "User"},
        )

        # Assert
        self.assertTrue("Hello User" in mail.outbox[0].body)

    @patch("core_main_app.utils.notifications.mail.SEND_EMAIL_ASYNC", True)
    @patch(
        "core_main_app.utils.notifications.tasks.task_mail.send_mail_to_website_contacts"
    )
    def test_send_async_mail_starts_a_task(self, mock_mail_task):
        """test_send_async_mail_starts_a_task"""
        # Arrange
        mock_mail_task.appy_async.return_value = None

        # Act
        send_mail_to_website_contacts(
            subject="test",
            path_to_template="mail.html",
            context={"username": "User"},
        )

        # Assert
        self.assertTrue(mock_mail_task.apply_async.called)

    @patch(
        "core_main_app.utils.notifications.tasks.task_mail.WEBSITE_CONTACTS",
        [],
    )
    def test_send_mail_without_contacts_does_not_send_email(
        self,
    ):
        """test_send_mail_without_contacts_does_not_send_email"""
        # Act
        send_mail_to_website_contacts(
            subject="test",
            path_to_template="mail.html",
            context={"username": "User"},
        )

        # Assert
        self.assertEqual(len(mail.outbox), 0)

    @patch(
        "core_main_app.utils.notifications.tasks.task_mail.WEBSITE_CONTACTS",
        [("test@example.com")],
    )
    def test_send_mail_website_contacts_setting_not_well_formatted_raise_value_error(
        self,
    ):
        """test_send_mail_without_contacts_does_not_send_email"""
        # Act + Assert
        with self.assertRaises(ValueError):
            send_mail_to_website_contacts(
                subject="test",
                path_to_template="mail.html",
                context={"username": "User"},
            )
        self.assertEqual(len(mail.outbox), 0)

    def test_send_mail_with_bad_template_rendering_does_not_send_email(
        self,
    ):
        """test_send_mail_without_contacts_does_not_send_email"""
        # Act
        send_mail_to_website_contacts(
            subject="test",
            path_to_template="wrong.html",
            context={"username": "User"},
        )
        # Assert
        self.assertEqual(len(mail.outbox), 0)
