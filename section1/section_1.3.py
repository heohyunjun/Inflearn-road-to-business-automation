import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
from googleapiclient import errors

def gmail_authenticate():
    SCOPES = ['https://mail.google.com/']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./private/credential.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def create_message(sender, to, subject, message_text, content_type = 'html'):
    message = EmailMessage()
    message.set_content(message_text, subtype=content_type)
    bcc_emails = "example1@example.com,example2@example.com"  # BCC 고정값 설정

    message["From"] = sender
    message["To"] = to.split(",")
    message['bcc'] = bcc_emails
    message["Subject"] = subject

    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8','surrogateescape')}

# 방금 추가한 코드 시작
def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print('Message Id: %s' % message['id'])
        return message
    
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
# 방금 추가한 코드 끝

def main():
    service = gmail_authenticate()
    sender = "hi.juuny@gmail.com"  # 보내는 사람 
    to = "hi.juuny@gmail.com"  # 받는 사람 
    subject = "Hello World!"  # 이메일 제목 
    message_text = "Hello, this is a test email."  # 이메일 본문

    message = create_message(sender, to, subject, message_text)
    send_message(service, "me", message)

if __name__ == '__main__':
    main()

