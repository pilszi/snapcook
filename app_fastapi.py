from fastapi import FastAPI

from static.oracle.db import connect
from src.job.detect_yolo import detect_img
from src.job.search_db import detect_foods, ing_names

app = FastAPI()


@app.get('/yolo/detection')
def detection(file:str):

    det_class = detect_img(file)
    # print(det_class)
    print(det_class)
    kor_class = [ing_names[x] for x in det_class]
    
    return kor_class


@app.post('/snapcook')
def snapcook(data:dict):
    print('='*60)
    print(data['class'])
    res = detect_foods(data['class'])
    
    return res


@app.get('/recipe/detail')
def detail(id:int):
    
    conn = connect()
    cur = conn.cursor()

    sql_a = """
        SELECT
            i.name as ing_name,
            b.value
        FROM food f JOIN basic_ingredients b ON b.food_id=f.id
            JOIN ingredients i ON i.id = b.ingredient_id
            WHERE f.id =:ids
    """
    sql_b = """
        SELECT
            recipe_step,
            recipe_text,
            image
        FROM recipe WHERE food_id =:ids
    """
    sql_c = """
        SELECT
            name,
            image
        FROM food WHERE id=:ids
    """
    
    cur.execute(sql_a, {"ids": id})
    basic_ing = cur.fetchall()
    # print(basic_ing)
    ingredient = [ing[0] for ing in basic_ing]
    values = [ing[1] for ing in basic_ing]

    cur.execute(sql_b, {'ids': id})
    recipes = cur.fetchall()
    # print(recipes)
    steps = [f'{r[0]}단계' for r in recipes]
    text = [r[1] for r in recipes]
    recipe_img = [r[2] for r in recipes]

    cur.execute(sql_c, {'ids': id})
    food_res = cur.fetchone()
    print(food_res)

    result = [ingredient, values, steps, text, recipe_img]
    print(result)

    return {'result': result, 'food': food_res}