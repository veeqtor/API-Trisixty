from django.core.mail import EmailMultiAlternatives


class EmailConcrete:
    """Email concrete for sending out email"""

    def send_email(self, subject, to, from_email=None, content=None, bcc=None):
        """Sends out emails

        Arguments:
            subject {str} -- Subject of the email
            to {list} -- Email to be Delivered
            bcc {list} -- BCC's
            from_email {str} -- Senders email
            content {str} -- Contents to be sent
        """

        from_email = 'Support <mailgun@sandbox1b552285ba6b49688aac0d7582ec23ff.mailgun.org>'
        # text_content = 'This is an important message.'
        html_content = f"""
        <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>repl.it</title>
                <link href="style.css" rel="stylesheet" type="text/css" />
            </head>
            <body>
                <a href="{content}">Activate</a> </br>
                <script src="script.js"></script>
            </body>
            </html>
        """
        email = EmailMultiAlternatives(
            subject,
            html_content,
            from_email,
            [to],
            bcc,
            reply_to=['nwokeochavictor@gmail.com'],
            headers={'Message-ID': 'foo'},
        )
        # email.content_subtype = "html"  # Main content is now text/html
        email.attach_alternative(html_content, "text/html")
        email.send()
