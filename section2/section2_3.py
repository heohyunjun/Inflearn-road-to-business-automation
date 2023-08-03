import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage
from googleapiclient import errors
import configparser
from collections import defaultdict
from each_mail_type import IntervieweUtility as IVU

class GmailUtils:
    # 방금 추가한 코드
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.service = self.gmail_authenticate()
    # 추가가 끝남

    def gmail_authenticate(self):
        SCOPES = ['https://mail.google.com/']
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                client_secret_path = self.config.get("Credential", "client_secrets")
                flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)


    def create_message(self, sender, to, subject, message_text, content_type = 'html'):
        message = EmailMessage()
        message.set_content(message_text, subtype=content_type)
        bcc_emails = self.config.get("Bcc", "bcc")
        message["From"] = sender
        message["To"] = to.split(",")
        message['bcc'] = bcc_emails
        message["Subject"] = subject

        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode('utf8','surrogateescape')}

    def send_message(self, user_id, message):
        try:
            message = self.service.users().messages().send(userId=user_id, body=message).execute()
            print('Message Id: %s' % message['id'])
            return message
        
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

def load_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def mail_type():
    mail_options = {
        1 : {
            'subject' : "[인프런] 서류 탈락 메일",
            'template' : "./templates/document_rejection_mail_template.html",
            'info_func' : IVU.required_info_for_document_rejection
        },
        2 : {
            'subject' : "[인프런] 면접 탈락 메일",
            'template' : "./templates/dropped_out_of_interview_email_template.html",
            'info_func' : IVU.required_info_for_interview_rejection
        },
        3 : {
            'subject' : "[인프런] 1차 면접 메일",
            'template' : "./templates/first_interview_email_template.html",
            'info_func' : IVU.required_info_for_first_interview
        },
        4 : {
            'subject' : "[인프런] 2차 면접 메일",
            'template' : "./templates/second_interview_email_template.html",
            'info_func' : IVU.required_info_for_second_interview
        }

    }
    return mail_options

def main():
    gmail = GmailUtils()

    config = configparser.ConfigParser()
    config.read('config.ini')
    sender = config.get("Sender","sender")

    to = "@gmail.com"  # 받는 사람 
    subject = "Hello World!"  # 이메일 제목 
    # message_text = "Hello, this is a test email."  # 이메일 본문
    message_text = load_template('./templates/second_interview_email_template.html')

    # message_text = message_text.format(
    #     이메일_받는_사람_이름 = '인프런수강생',
    #     금번_채용_공고명 = '마켓팅 채용',
    #     몇차_채용인지 = '1',
    #     다음_인터뷰_날짜 = '2023년 12월 12일'
    # )

    # 언팩킹
    # required_info = defaultdict()
    # required_info['이메일_받는_사람_이름'] = '인프런수강생'
    # required_info['금번_채용_공고명'] = '마켓팅 채용'
    # required_info['몇차_채용인지'] = '1'
    # required_info['다음_인터뷰_날짜'] = '2023년 12월 12일'
    # message_text = message_text.format(**required_info)


    mail_options = mail_type()
    print(f"번호를 선택하세요")
    for key, value in mail_options.items():
        print(f"{key}, {value['subject']}")
    
    num = int(input("메일 타입: "))
    if num not in mail_options:
        raise ValueError("번호가 틀림")
    
    option = mail_options[num]
    subject = option['subject']
    mail_template = option['template']

    required_info = option['info_func']()
    to = input("수신자 이메일: ")

    mail_template = load_template(mail_template)
    message_text = mail_template.format(**required_info)
    message = gmail.create_message(sender, to, subject, message_text)

    gmail.send_message("me", message)
if __name__ == '__main__':
    main()

