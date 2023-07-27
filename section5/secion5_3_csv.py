import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime
import pandas as pd


urllib3.disable_warnings()

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

# 각각의 값을 저장할 리스트
title_list, date_list, link_list = [], [], []

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

    # 밑으로는 동일

    # 1페이지에서만 뉴스를 가져오는 중
    for news in news_items:
        # 날짜
        news_date = news.find('span', {'class' : 'news_writer'})
        news_date = news_date.text
        news_date = news_date.split("|")[-1].strip()
        crawled_date = datetime.strptime(news_date, "%Y년 %m월 %d일 %H:%M")

        if today.date() == crawled_date.date():
            # print("크롤링한 데이터의 날짜가 오늘 날짜입니다")
            news_a_tage = news.select_one('a')

            # 링크
            link = news_a_tage['href']
            
            # 제목
            title = news_a_tage.select_one('span').text

            # 리스트에 값 추가
            title_list.append(title)
            date_list.append(news_date)
            link_list.append(main_url+link)
            
        else:
            print("크롤링한 데이터의 날짜가 오늘 날짜가 아닙니다.")
            break_flag = True
            break
        print("========================")
    if break_flag:
        break
        
# 리스트를 사용해서 데이터 프레임 생성
df = pd.DataFrame(
    {
        "뉴스 제목" : title_list,
        "뉴스 날짜" : date_list,
        "뉴스 링크" : link_list
    }
)
print(df)
df.to_csv("news_data.csv", index=False)