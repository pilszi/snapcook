from fastapi import FastAPI

from static.oracle.db import connect

app = FastAPI()


@app.get('/snapcook')
def snapcook(ing:str):

    conn = connect()
    cur = conn.cursor()

    sql_a = """
        SELECT
            f.id,
            f.name as food_name,
            f.image as food_img,
            i.name
        FROM ing_name ig JOIN ingredients i ON ig.ing_id=i.id
            JOIN basic_ingredients b ON b.ingredient_id= i.id
            JOIN food f ON f.id= b.food_id
            WHERE ig.en_name=:ing AND f.name LIKE '%' || i.name || '%'
    """
    cur.execute(sql_a, {'ing': ing})
    rows = cur.fetchall()
    print(len(rows))
    ids = [row[0] for row in rows]
    title = [row[1] for row in rows]
    img = [row[2] for row in rows]
    result = [title, img, ids]
    ing_kr = rows[0][3]

    return {'result': result, 'ing': ing_kr}

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