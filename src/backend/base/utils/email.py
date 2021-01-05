import logging
import os
import os.path

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Sending Email

logger = logging.getLogger(__name__)


def send(to_mail, subject, html_body, text_body=None, attachments=[], from_email=None, mail_cc=None, bcc=None):
    if not isinstance(to_mail, (list, tuple)):
        to_mail = [to_mail]

    # Remove empty items
    to_mail = [x for x in to_mail if x not in (None, "")]

    if text_body is None:
        text_body = strip_tags(html_body)

    # Convert CC into a list
    if mail_cc and not isinstance(mail_cc, (list, tuple)):
        mail_cc = [mail_cc]

    # Convert BCC into a list
    if bcc and not isinstance(bcc, (list, tuple)):
        bcc = [bcc]

    # if bcc is None, set a default email as bcc
    if not bcc:
        bcc = []

    try:
        msg = EmailMultiAlternatives(subject, text_body, to=to_mail)
        if mail_cc:
            msg.cc = mail_cc

        if bcc:
            msg.bcc = bcc

        if from_email:
            msg.from_email = from_email

        msg.attach_alternative(html_body, "text/html")
        for attachment in attachments:
            if attachment:
                # Try to get only filename from full-path
                try:
                    attachment.open()
                except Exception as except_str:
                    print(str(except_str))
                attachment_name = os.path.split(attachment.name)[-1]
                msg.attach(attachment_name or attachment.name, attachment.read())
        msg.send()
        return True
    except Exception as except_str:
        logger.exception("Unable to send the mail." + str(except_str))
    return False


def send_from_template(mail_to, subject, template, context, **kwargs):
    # print template
    html_body = render_to_string(template, context)
    return send(mail_to, subject, html_body, **kwargs)


def order_placed_email(sale_obj):
    print(sale_obj)
