import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..", "..")
sys.path.append(os.path.abspath(parent_dir))

from static.oracle.db import connect

conn = connect()
cur = conn.cursor()

vegetables_korean_map = {
    'broccoli': ['브로콜리'],
    'cabbage': ['양배추'],
    'carrot': ['당근'],
    'chili': ['고추', '청양고추', '홍고추', '꽈리고추', '풋고추', '페페론치노', '건고추', '오이고추'],
    'corn': ['옥수수', '옥수수콘', '캔옥수수', '삶은 옥수수'],
    'cucumber': ['오이', '백오이'],
    'egg': ['달걀', '계란', '삶은달걀', '삶은 달걀', '달걀 노른자', '달걀노른자', '달걀 흰자', '달걀흰자'],
    'green onion': ['대파', '쪽파', '파'],
    'mushroom': ['버섯', '표고버섯', '팽이버섯', '느타리버섯'],
    'onion': ['양파', '적양파'],
    'bell pepper': ['피망', '파프리카'],
    'potato': ['감자'],
    'radish': ['무'],
    'squash': ['애호박', '호박', '단호박', '늙은호박'],
    'beans': ['콩', '완두콩'],
    'beetroot': ['비트'],
    'cauliflower': ['콜리플라워'],
    'coriander': ['고수'],
    'eggplant': ['가지'],
    'garlic': ['마늘', '다진마늘', '다진 마늘', '깐마늘', '통마늘'],
    'ginger': ['생강', '다진생강', '다진 생강'],
    'lettuce': ['상추'],
    'spinach': ['시금치'],
    'sweetpotato': ['고구마'],
    'tomato': ['토마토', '방울토마토', '대저토마토', '완숙토마토']
}

sql_i = "INSERT INTO ing_name (ING_ID, EN_NAME) SELECT ID, :en_name FROM ingredients WHERE NAME = :kr_name"
print("-- DB 실행용 INSERT SQL --")
for en_name, kr_list in vegetables_korean_map.items():
    for kr_name in kr_list:
        # print(en_name+ ' / '+ kr_name)
        cur.execute("SELECT COUNT(*) FROM ing_name WHERE en_name=:en_name", {'en_name':en_name})
        row = cur.fetchone()
        # print(row[0])
        if row[0] == 0:
            cur.execute(sql_i, {'en_name': en_name, 'kr_name': kr_name})
            result = cur.rowcount
            print(result)
conn.commit()
print('저장 완료')