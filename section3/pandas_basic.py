import pandas as pd

email_dataframe = pd.read_csv("email.csv", encoding="utf-8")
# print(email_dataframe)

# row 하나씩 for문을 돌면서, 각각의 정보들을 required_info 만드는데 사용할 것

# 각 줄의 정보를 출력
for index, row in email_dataframe.iterrows():
    print(index)
    #print(row)
    # row 는 6개의 정보를 지니고있음
    # 언패킹
    이름, 공고명, 몇차면접, 인터뷰날짜, 이메일, 메일유형 = row

    # 확인
    print(이름)
    print("====================")