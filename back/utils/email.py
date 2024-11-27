import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail



def send_email(to, subject, content):
    message = Mail(
        from_email='dnadares@gmail.com',
        to_emails='fdarias@fi.uba.ar',
        subject='Sending with Twilio SendGrid is Fun',
        html_content='<strong>and easy to do anywhere, even with Python</strong>')
    try:
        print(os.environ.get('SENDGRID_API_KEY'))
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
