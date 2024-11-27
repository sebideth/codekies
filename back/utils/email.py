import os
import logging

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

logger = logging.getLogger(__name__)


def send_email(to, subject, content):
    try:
        message = Mail(
            from_email=os.environ.get('SENDER'),
            to_emails=to,
            subject=subject,
            html_content=content
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logger.debug(response.status_code)
        logger.debug(response.body)
        logger.debug(response.headers)
        return True
    except Exception as e:
        logger.error(e)
        return False
