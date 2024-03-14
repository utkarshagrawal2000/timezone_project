from django.core.mail import EmailMessage
import os
import datetime
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

class Util:
  @staticmethod
  def send_email(data):
    email = EmailMessage(
      subject=data['subject'],
      body=data['body'],
      from_email=os.environ.get('EMAIL_FROM'),
      to=[data['to_email']]
    )
    email.send()

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print("bbbbbbbbbbbbbbbbb")
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    print('1')
    API_SERVICE_NAME = api_name
    print('2')
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print('3')
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    print(pickle_file)
    print('4')
    if os.path.exists(pickle_file):
        print('5')
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
        print(cred,'cred')
    print('6')
    if not cred or not cred.valid:
        print('7')
        if cred and cred.expired and cred.refresh_token:
            print('8')
            cred.refresh(Request())
            print('9')
        else:
            print('10')
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            print('100000000')
            cred = flow.run_local_server()
            print(cred,'ddd')
            print('11')

        with open(pickle_file, 'wb') as token:
            print('12')
            pickle.dump(cred, token)
            print('13')
    print('13')
    try:
        print('check111111111111111')
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
