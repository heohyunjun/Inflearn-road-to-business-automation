import requests
from bs4 import BeautifulSoup
import urllib3
from datetime import datetime

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



# 3.6 모든 기사의 뉴스 제목, 링크, 날짜 출력
for news in news_items:
    # 날짜
    news_date = news.find('span', {'class' : 'news_writer'})
    news_date = news_date.text
    news_date = news_date.split("|")[-1].strip()
    crawled_date = datetime.strptime(news_date, "%Y년 %m월 %d일 %H:%M")
    if today.date() == crawled_date.date():
        print("크롤링한 데이터의 날짜가 오늘 날짜입니다")
        news_a_tage = news.select_one('a')

        # 링크
        link = news_a_tage['href']
        
        # 제목
        title = news_a_tage.select_one('span').text
        print(title)
        print(news_date)
        print(link)
        
    else:
        print("크롤링한 데이터의 날짜가 오늘 날짜가 아닙니다.")
    print("========================")




