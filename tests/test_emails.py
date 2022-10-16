import os
import unittest
from unittest.mock import patch

from .context import nmdmail

EMAIL_DIR = os.path.join(os.path.dirname(__file__), "emails")


class TestEMails(unittest.TestCase):
    def validate_email_content(self, email_file, html=None, text=None):
        email_file = os.path.join(EMAIL_DIR, email_file)
        with open(email_file) as f:
            email_content = f.read()
        image_root = os.path.dirname(email_file)
        email = nmdmail.EmailContent(email_content, image_root=image_root)

        if html:
            with open(os.path.join(EMAIL_DIR, html)) as f:
                html = f.read()
            self.assertEqual(email.html.strip(), html.strip(), msg="HTML output mismatch")

        if text:
            with open(os.path.join(EMAIL_DIR, text)) as f:
                text = f.read()
            self.assertEqual(email.text.strip(), text.strip(), msg="Plain text output mismatch")

        return email

    def test_basic(self):
        self.validate_email_content("basic.md", html="basic.html", text="basic.txt")

    def test_unicode(self):
        self.validate_email_content(
            "unicode.md", html="unicode.html", text="unicode.txt"
        )

    @patch("emails.Message")
    def test_email_with_headers(self, message_mock):
        email = self.validate_email_content(
            "email_headers.md", html="email_headers.html", text="email_headers.txt"
        )
        nmdmail.send(email)
        message_args = message_mock.call_args[1]
        self.assertEqual(message_args["subject"], "Email Header Test")
        self.assertEqual(message_args["mail_from"], "from@test.com")
        self.assertEqual(message_args["mail_to"], "to@test.com")
        self.assertEqual(message_args["cc"], ["cc1@test.com", "cc2@test.com"])
        self.assertEqual(message_args["bcc"], "bcc@test.com")
        self.assertEqual(message_args["headers"], {"reply-to": "reply-to@test.com"})


if __name__ == "__main__":
    unittest.main()
