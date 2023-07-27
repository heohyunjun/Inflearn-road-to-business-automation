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
import pandas as pd
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

def mail_type(이름, 공고명, 몇차면접, 인터뷰날짜, 메일유형):
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

    # 메일 유형 번호 선택
    # 메일 유형은 현재 "1" 과 같이 문자열 형태, 따라서 int를 사용
    num = int(메일유형)

    # 번호가 틀린 경우(1~4번 이외의 번호를 선택한 경우 에러 발생)
    if num not in mail_options:
        raise ValueError("번호가 틀림")
    

    option = mail_options[num]
    subject = option['subject']
    mail_template = option['template']

    # 함수 인자값으로 값을 넘겨줌
    required_info = option['info_func'](이름, 공고명, 몇차면접, 인터뷰날짜)


    return subject, mail_template, required_info


def main():
    gmail = GmailUtils()

    config = configparser.ConfigParser()
    config.read('config.ini')
    sender = config.get("Sender","sender")

    email_dataframe = pd.read_csv("email.csv", encoding='utf-8')

    # section 3.3 
    for index, row in email_dataframe.iterrows():
        이름, 공고명, 몇차면접, 인터뷰날짜, 이메일, 메일유형 = row

        subject, mail_template, required_info = mail_type(이름, 공고명,
                                                          몇차면접, 인터뷰날짜,
                                                          메일유형)


        mail_template = load_template(mail_template)
        message_text = mail_template.format(**required_info)

        to = 이메일
        message = gmail.create_message(sender, to, subject, message_text)

        gmail.send_message("me", message)
        
if __name__ == '__main__':
    main()

