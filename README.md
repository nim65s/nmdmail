# nMdmail: Send emails written in Markdown

Fork of https://github.com/yejianye/mdmail, which looks dead.

[![PyPI version](https://badge.fury.io/py/nmdmail.svg)](https://pypi.org/project/nmdmail)
[![Tests](https://github.com/nim65s/nmdmail/actions/workflows/test.yml/badge.svg)](https://github.com/nim65s/nmdmail/actions/workflows/test.yml)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/nim65s/nmdmail/main.svg)](https://results.pre-commit.ci/latest/github/nim65s/nmdmail/main)
[![codecov](https://codecov.io/gh/nim65s/nmdmail/branch/main/graph/badge.svg?token=BLGISGCYKG)](https://codecov.io/gh/nim65s/nmdmail)
[![Maintainability](https://api.codeclimate.com/v1/badges/6737a84239590ddc0d1e/maintainability)](https://codeclimate.com/github/nim65s/nmdmail/maintainability)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


nMdmail sends emails written in Markdown. It could be used as a standalone command-line script or as a python module. The features includes

- Have a sane default CSS style and support CSS customization
- Support local images as inline images

Screenshot of an email sent via nmdmail viewed in Google Inbox

<img src="screenshot.png" height="640"></img>

To install nmdmail

```bash
$ python -m pip install nmdmail
```

## Send Email in Command-line

When sending emails from command-line, the body of the email could be read from a file or stdin.

Email headers such as subject, from/to, cc etc could be specified at the beginning of the markdown file, Or be specified in command-line arguments.

Here is an example of Markdown file with email headers

```
Subject: Sample Email
From: foo@xyz.com
To: bar@xyz.com
Cc: baz@xyz.com

# Sample Email

-

![Embed local image](../assets/image.jpg)
```

To send this email with nmdmail

```bash
$ nmdmail sample_email.md
```

Here is an example of specifying subject, from/to in command-line

```bash
$ nmdmail --from=foo@xyz.com --to=bar@xyz.com --subject='Sample' sample_email.md
```

To read email content from stdin,

```bash
$ echo '# Sample Email' | nmdmail --from=foo@xyz.com --to=bar@xyz.com --subject='Sample'
```

SMTP server configurations are read from the following environment variables

```bash
export MDMAIL_HOST="" # default: localhost
export MDMAIL_PORT="" # default: 25
export MDMAIL_USE_TLS="" # default: false
export MDMAIL_USE_SSL="" # default: false
export MDMAIL_USERNAME="" # default: None
export MDMAIL_PASSWORD="" # default: None
export MDMAIL_DEFAULT_SENDER="" # default: None
```

Full help of `nmdmail` command-line script

```bash
usage: nmdmail [-h] [--subject SUBJECT] [--from FROM_] [--to TO] [--cc CC]
               [--bcc BCC] [--reply-to REPLY_TO] [--css CSS] [--print-only]
               [file]

Send email written in Markdown.

positional arguments:
  file                  Markdown file for email content. Default to STDIN.

optional arguments:
  -h, --help            show this help message and exit
  --subject SUBJECT, -s SUBJECT
                        Subject line
  --from FROM, -f FROM
                        From address
  --to TO, -t TO        To addresses, separated by comma
  --cc CC, -c CC        CC address, separated by comma
  --bcc BCC, -b BCC     Bcc address, separated by comma
  --reply-to REPLY_TO, -r REPLY_TO
                        Reply-to address
  --css CSS             Use a custom CSS file
  --print-only, -p      Only print out rendered html
```

## Send Email in Python Code

Sending emails in python is straight-forward.

```python
import nmdmail

email="""
# Sample Email

- Python is awesome
- Markdown is cool

![Embed local image](../assets/image.jpg)
"""

nmdmail.send(email, subject='Sample Email',
            from_email='foo@example.com', to_email='bar@example.com')
```

By default, it will use SMTP server on localhost. You could specify a SMTP server as well.

```python
# Specify SMTP server
smtp = {
  'host: 'my-mailserver.com',
  'port': 25,
  'tls': False,
  'ssl': False,
  'user: '',
  'password': '',
}

nmdmail.send(content,
             subject='Sample Email',
             from_email='foo@example.com',
             to_email='bar@example.com',
             smtp=smtp)
```


### API documentation `nmdmail.send`

- **email** (str/obj): A markdown string or EmailContent object
- **subject** (str): subject line
- **from_email** (str): sender email address
- **to_email** (str/list): recipient email addresses
- **cc** (str/list): CC email addresses (string or a list)
- **bcc** (str/list): BCC email addresses (string or a list)
- **reply_to** (str): Reply-to email address
- **smtp** (dict): SMTP configuration with following keys
    - *host* (str): SMTP server host. Default: localhost
    - *port* (int): SMTP server port. Default: 25
    - *tls* (bool): Use TLS. Default: False
    - *ssl* (bool): Use SSL. Default: False
    - *user* (bool): SMTP login user. Default empty
    - *password* (bool): SMTP login password. Default empty

## Use nmdmail with Vim and Emacs

Since `nmdmail` can read from stdin and support email headers such as subject/from/to in the markdown file itself,
integrating nmdmail with Vim, Emacs or other text editors is easy.

To use nmdmail in Vim, just write a markdown email with headers, and then execute `w !nmdmail` command, which will send
current buffer as stdin to nmdmail.

In Emacs, you could write a small function to do the same thing

```lisp
(defun nmdmail-send-buffer ()
  (interactive)
  (shell-command-on-region (point-min) (point-max) "nmdmail"))
```

Then `M-x nmdmail-send-buffer` will send current buffer to nmdmail.
