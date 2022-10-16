import os
import unittest
from unittest.mock import patch

from .context import cli

os.environ.update(
    {
        "MDMAIL_HOST": "smtp.test.com",
        "MDMAIL_PORT": "25",
        "MDMAIL_USE_TLS": "0",
        "MDMAIL_USE_SSL": "0",
        "MDMAIL_USERNAME": "",
        "MDMAIL_PASSWORD": "",
        "MDMAIL_DEFAULT_SENDER": "default@test.com",
    }
)


class StdinMock:
    def read(self):
        return "Content from Stdin"


class TestCli(unittest.TestCase):
    @patch("nmdmail.send")
    def test_cli(self, send_mock):
        md_file = os.path.join(os.path.dirname(__file__), "emails/basic.md")
        cli.main(
            [
                "--subject",
                "Hello World",
                "--from=from@test.com",
                "--to=to@test.com",
                "--cc=cc@test.com",
                "--bcc=bcc@test.com",
                "--reply-to=reply-to@test.com",
                md_file,
            ]
        )
        self.assertEqual(
            send_mock.call_args[1],
            {
                "subject": "Hello World",
                "from_email": "from@test.com",
                "reply_to": "reply-to@test.com",
                "to_email": "to@test.com",
                "cc": "cc@test.com",
                "bcc": "bcc@test.com",
                "smtp": {
                    "host": "smtp.test.com",
                    "port": 25,
                    "user": "",
                    "password": "",
                    "tls": False,
                    "ssl": False,
                },
            },
        )

    @patch("nmdmail.send")
    def test_default_sender(self, send_mock):
        md_file = os.path.join(os.path.dirname(__file__), "emails/basic.md")
        cli.main(["--subject", "Hello World", "--to=to@test.com", md_file])
        self.assertEqual(send_mock.call_args[1]["from_email"], "default@test.com")

    @patch("sys.stdin", new_callable=StdinMock)
    @patch("nmdmail.EmailContent")
    @patch("nmdmail.send")
    def test_read_from_stdin(self, send_mock, email_mock, stdin_mock):
        cli.main(["--subject", "Hello World", "--to=to@test.com"])
        self.assertEqual(email_mock.call_args[0], ("Content from Stdin",))

    @patch("nmdmail.send")
    def test_print_only(self, send_mock):
        md_file = os.path.join(os.path.dirname(__file__), "emails/basic.md")
        cli.main(
            ["--subject", "Hello World", "--to=to@test.com", "--print-only", md_file]
        )
        send_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
