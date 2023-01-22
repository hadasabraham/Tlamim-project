from __future__ import print_function

import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.message import EmailMessage
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']


class EmailServer(object):

    def __init__(self):
        self.__service = None
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{os.getcwd()}{os.path.sep}emails{os.path.sep}token.json'):
            creds = Credentials.from_authorized_user_file(f'{os.getcwd()}{os.path.sep}emails{os.path.sep}token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{os.getcwd()}{os.path.sep}emails{os.path.sep}credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(f'{os.getcwd()}{os.path.sep}emails{os.path.sep}token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            self.__service = build('gmail', 'v1', credentials=creds)
        except Exception as e:
            print("Got exception gmail api", e)

    def send_email(self, to_email: str, from_email: str, subject: str, content: str):
        if self.__service:
            try:
                message = EmailMessage()
                message.set_content(content)
                message['To'] = to_email
                message['From'] = from_email
                message['Subject'] = subject

                # encoded message
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                    .decode()

                create_message = {
                    'raw': encoded_message
                }
                # pylint: disable=E1101
                send_message = self.__service.users().messages().send(userId="me", body=create_message).execute()
                print(F'Message Id: {send_message["id"]}')
            except HttpError as error:
                print(F'An error occurred: {error}')