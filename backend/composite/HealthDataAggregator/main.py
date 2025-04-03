import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

message = Mail(from_email = 'ecosmart.diet@gmail.com',
               to_emails = 'zephanchin123@gmail.com',
               subject = 'Monthly Report Stats',
               plain_text_content = 'Ran for 30 mins and burnt 120 calories',
               html_content = '<strong>Ran for 30 mins and burnt 120 calories</strong>')
# try:
sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])
response = sg.send(message)
print(response.status_code)
# print(response.body)
# print(response.headers)
# except Exception as e:
#     print(e.message)
