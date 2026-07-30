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
    'chili': ['고추', '페페론치노'],
    'corn': ['옥수수'],
    'cucumber': ['오이'],
    'egg': ['달걀', '계란'],
    'green onion': ['대파', '쪽파'],
    'mushroom': ['버섯'],
    'onion': ['양파'],
    'paprika': ['피망', '파프리카'],
    'potato': ['감자'],
    'radish': ['무'],
    'squash': ['호박'],
    'beans': ['콩', '서리태'],
    'beetroot': ['비트'],
    'cauliflower': ['콜리플라워'],
    'coriander': ['고수'],
    'eggplant': ['가지'],
    'garlic': ['마늘'],
    'ginger': ['생강'],
    'lettuce': ['상추'],
    'spinach': ['시금치'],
    'sweetpotato': ['고구마'],
    'tomato': ['토마토']
}

sql_i = "INSERT INTO ing_name (ING_ID, EN_NAME) SELECT ID, :en_name FROM ingredients WHERE name = :kr_name"
print("-- DB 실행용 INSERT SQL --")
for en_name, kr_list in vegetables_korean_map.items():
    for kr_name in kr_list:
        # print(en_name+ ' / '+ kr_name)
        sql_s = """SELECT 
            count(*) 
        FROM ing_name ig JOIN ingredients i ON ig.ing_id=i.id 
            WHERE i.name = :1"""
        cur.execute(sql_s, [kr_name])
        row = cur.fetchone()
        # print(row[0])
        if row[0] == 0:
            cur.execute(sql_i, {'en_name': en_name, 'kr_name': kr_name})
            result = cur.rowcount
            print(f'{result} / {kr_name}')
conn.commit()
print('저장 완료')