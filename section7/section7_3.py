import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime
import pandas as pd

import os
# 슬랙볼트 임포트하기
from slack_bolt import App

if __name__ == __main__:
        

    urllib3.disable_warnings()

    slack_token = os.environ.get("SLACK_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL")

    # 슬랙 앱 인스턴스 초기화
    app = App(token=slack_token)

    # 1. 사이트분석
    main_url = 'https://www.boannews.com'
    news_list_url = '/media/t_list.asp'
    response = requests.get(main_url + news_list_url, verify=False)
    soup = BeautifulSoup(response.text, "html.parser")


    # 3. 전체 뉴스 기사의 제목 가져오기
    # 3.1 news_area 내용을 전부 가져온다
    news_area_selector = '#news_area'
    news_area = soup.select_one(news_area_selector)

    # 3.2 news_area에서 news_list를 가져온다
    news_items = news_area.select('div.news_list')

    # 오늘 날짜 출력
    today = datetime.today()

    # 크롤링 중단
    break_flag = False
    for i in range(1, 11):
        # 각 페이지 주소 생성
        news_page_url = f'https://www.boannews.com/media/t_list.asp?Page={i}&kind='
        
        response = requests.get(news_page_url, verify=False)
        soup = BeautifulSoup(response.text, "html.parser")

        # 각 페이지의 news_area 내용 가져오기
        news_area_selector = '#news_area'
        news_area = soup.select_one(news_area_selector)

        # news_area에서 news_list를 가져온다
        news_items = news_area.select('div.news_list')

        # 뉴스가 없는 경우
        news_found= False

        # 1페이지에서만 뉴스를 가져오는 중
        for news in news_items:
            # 날짜
            news_date = news.find('span', {'class' : 'news_writer'})
            news_date = news_date.text
            news_date = news_date.split("|")[-1].strip()
            crawled_date = datetime.strptime(news_date, "%Y년 %m월 %d일 %H:%M")

            if today.date() == crawled_date.date():
                news_found = True
                # print("크롤링한 데이터의 날짜가 오늘 날짜입니다")
                news_a_tage = news.select_one('a')

                # 링크
                link = news_a_tage['href']
                
                # 제목
                title = news_a_tage.select_one('span').text

                
                message = f"날짜: {news_date}\n링크: {main_url +link}\n제목: {title}"

                slack_response = app.client.chat_postMessage(channel=slack_channel,
                                                            text = message)
            else:
                print("크롤링한 데이터의 날짜가 오늘 날짜가 아닙니다.")
                break_flag = True
                break
            print("========================")
        if break_flag:
            break

    # 뉴스가 없는 경우
    if not news_found:
        slack_response = app.client.chat_postMessage(channel=slack_channel,
                                            text = "뉴스가 없습니다")