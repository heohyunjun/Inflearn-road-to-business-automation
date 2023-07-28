from dotenv import load_dotenv
import os

# 슬랙볼트 임포트하기
from slack_bolt import App

load_dotenv()

slack_token = os.getenv("SLACK_TOEKN")
slack_channel = os.getenv("SLACK_CHANNEL")

# 슬랙에 메시지 보내기

app = App(token=slack_token)
response = app.client.chat_postMessage(
    channel=slack_channel,
    text = '크롤링 결과 슬랙으로 전송하기 실습'
)

if response['ok']:
    print("전송완료")
else:
    print("전송실패")