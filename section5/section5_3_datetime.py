from datetime import datetime

# 1. 오늘 날짜 출력
today = datetime.today()
print(type(today))

crawled_date_str = '2023년 07월 27일 12:41'
print(type(crawled_date_str))

# 두 날짜를 비교하기 위해서, 크롤링된 날짜 문자열을 날짜형식으로 변환
crawled_date = datetime.strptime(crawled_date_str, "%Y년 %m월 %d일 %H:%M")
print(type(crawled_date))

# 년,월, 일 만 비교하고 시간은 필요없음
print(today.date())

if today.date() == crawled_date.date():
    print("크롤링한 데이터의 날짜가 오늘 날짜입니다")
else:
    print("크롤링한 데이터의 날짜가 오늘 날짜가 아닙니다.")