import os
import sys
# 현재 파일(recipe.py)의 부모의 부모 폴더(상위 폴더) 경로를 구해 시스템 경로에 추가합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, "..", "..") # src 폴더 외부의 루트(SNAPCOOK)까지 올라감
sys.path.append(os.path.abspath(parent_dir))

from bs4 import BeautifulSoup
import requests
import json
from static.oracle.db import connect
import time

conn = connect()

sql = 'SELECT link FROM recipe_link'

cur = conn.cursor()
cur.execute(sql)
link_elems = cur.fetchall()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 Safari/537.36"
}
# 연결 통로 유지
session = requests.Session()
session.headers.update(headers)
for link in link_elems:
    food_recipe = {}
    response = session.get(link[0])
    soup = BeautifulSoup(response.text, "html.parser")
    next_data_script = soup.find("script", id="__NEXT_DATA__")
    if next_data_script:
        data = json.loads(next_data_script.string)
        try:
            # 1. 확인한 레시피 경로로 들어갑니다. (recipe -> recipe_steps)
            recipe_info = data['props']['pageProps']['recipe']
            food_recipe['image'] = soup.find("meta", property="og:image").get('content', "")
            food_recipe['title'] = recipe_info['title']
            ingredients = recipe_info['recipe_igroups']
            food_recipe['level'] = recipe_info['level']
            name = ''
            value = ''
            group = []
            for items in ingredients:
                # print(items)
                for item in items['ingredients']:
                    # print(item)
                    name = item['name'].strip()
                    value = item['value'].strip()
                    group.append([name, value])
            food_recipe['ingredients'] = group
            # print(f"{title} / {group}")
            steps = recipe_info['recipe_steps']
            print(f"==== 찾아낸 {recipe_info['title']} 레시피 단계: {len(steps)}개 ====")
            recipe_steps = []
            # 2. 각 단계별로 데이터를 순서대로 뽑아줍니다.
            for idx, step in enumerate(steps):
                text = step.get('content', '')
                image_url = ""
                imgs_list = step.get('imgs', [])
                
                if imgs_list:
                    try:
                        # imgs 안의 첫 번째 요소가 JSON 문자열이므로, json.loads()로 변환
                        img_data = json.loads(imgs_list[0])
                        # print(imgs_list[0])
                        # print(img_data)
                        image_url = img_data.get('img', '')
                    except Exception:
                        # 혹시 일반 문자열일 경우를 대비한 안전장치
                        image_url = imgs_list[0]
                # 수집한 데이터 리스트에 담기
                recipe_steps.append({
                    "step_num": idx + 1,
                    "text": text,
                    "image": image_url
                })
                food_recipe['steps'] = recipe_steps
                # 출력 확인
                # print(f"Step {idx + 1}")
                # print(f"설명: {text}")
                # if image_url:
                #     print(f"이미지: {image_url}")
            try:
                cur.execute("""SELECT id FROM food WHERE name = :1""", [food_recipe['title'],])
                food_result = cur.fetchone()
                food_id = ''
                if food_result is not None:
                    food_id = food_result[0]
                    print(f"{food_recipe['title']} 은 이미 저장 되었습니다.")
                else:
                    food_id_var = cur.var(int)  
                    sql = """INSERT INTO food(name, image, food_level)VALUES(:1, :2, :3) RETURNING id INTO :4"""
                    cur.execute(sql, [food_recipe['title'], food_recipe['image'], food_recipe['level'], food_id_var])
                    food_id = food_id_var.getvalue()[0]
                # print(food_id)
                
                # print(food_recipe['steps'])
                cur.execute("""SELECT count(food_id) FROM recipe WHERE food_id = :1""", [food_id,])
                recipe_result = cur.fetchone()
                if recipe_result[0] == 0:
                    sql = "INSERT INTO recipe(food_id, recipe_step, recipe_text, image)VALUES(:1, :2, :3, :4)"
                    for items in food_recipe['steps']:
                        # print(f"{items['step_num']}단계")
                        cur.execute(sql, [food_id, items['step_num'], items['text'], items['image']])

                ing_id = ''
                for item in food_recipe['ingredients']:
                    # print(food_recipe['ingredients'][i][0])
                    cur.execute("""SELECT id FROM ingredients WHERE name = :1""", [item[0],])
                    ing_result = cur.fetchone()
                    if ing_result is not None:
                        ing_id = ing_result[0]
                    else:
                        ing_id_var = cur.var(int)
                        sql = "INSERT INTO ingredients(name)VALUES(:1) RETURNING id INTO :2"
                        cur.execute(sql, [item[0], ing_id_var])
                        ing_id = ing_id_var.getvalue()[0]
                    # print(ing_id)

                    cur.execute("""SELECT count(*) FROM basic_ing WHERE food_id = :1 AND ing_id = :2""", [food_id, ing_id])
                    basic_result = cur.fetchone()
                    if basic_result[0] == 0:
                        sql = """INSERT INTO basic_ing(food_id, ing_id, value)VALUES(:1, :2, :3)"""
                        cur.execute(sql, [food_id, ing_id, item[1]])  

                conn.commit()
                print(f"==== {food_recipe['title']} DB 저장 완료 ====")
                print("=" * 60)
            except Exception as e:
                sql = "INSERT INTO fail_link(link)VALUES(:1)"
                cur.execute(sql, [link[0]])
                conn.commit()
                print(f"에러 발생으로 DB 저장 건너 뜁니다({link[0]}) : {e}")
            
        except KeyError as e:
            print(f"❌ 데이터를 찾아가는 중 오류가 발생했습니다: {e}")
    else:
        print("❌ __NEXT_DATA__ 스크립트를 찾을 수 없습니다.")
    time.sleep(1)
conn.close()