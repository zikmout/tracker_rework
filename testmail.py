import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SERVICE_ACCOUNT_FILE = './arf.json'
# SERVICE_ACCOUNT_FILE = "./client_secret.json"
print("Test Mail2.py")
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# delegated_credentials = creds.with_subject('simon.sicard@gmail.com')
service = build('gmail', 'v1', credentials=creds)
message = MIMEText('This is the body of the email')
message['from'] = 'simon.sicard@gmail.com'
message['to'] = 'simon@bridg-it.fr'
message['subject'] = 'Email Subject'
create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

try:
    message = (service.users().messages().send(
        userId="me", body=create_message).execute())
    print(F'sent message to {message} Message Id: {message["id"]}')
except HTTPError as error:
    print(F'An error occurred: {error}')
    message = None
