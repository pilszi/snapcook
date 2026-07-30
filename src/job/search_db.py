from static.oracle.db import connect

ing_names = {}

try:
    cur = connect().cursor()
    cur.execute("""SELECT i.name, ig.en_name FROM ing_name ig JOIN ingredients i ON i.id = ig.ing_id""")
    ing_res = cur.fetchall()
    for kr_name, en_name in ing_res:
        if en_name not in ing_names:
            ing_names[en_name] = []
        ing_names[en_name].append(kr_name)
    cur.close()
    print(ing_names)
except Exception as e:
    print(e)


def detect_foods(cls):

    count_target = len(cls) # 2개
    bind_names = ', '.join(f":{i}" for i in range(count_target))
    sql_b = f"""
    SELECT 
        f.name, 
        f.image, 
        f.id,
        f.food_level,
        COUNT(DISTINCT i.id) AS match_count
    FROM food f
        JOIN basic_ing b ON f.id = b.food_id
        JOIN ingredients i ON i.id = b.ing_id
            WHERE REGEXP_LIKE(i.name, :1)
            GROUP BY f.id, f.name, f.image, f.food_level
            ORDER BY match_count DESC, f.name ASC
    """
    with connect().cursor() as cur:
        cur.execute(sql_b, ['|'.join(cls)]) 
        res = cur.fetchall()
    title = [r[0] for r in res]
    img = [r[1] for r in res]
    ids = [r[2] for r in res]
    levels = [r[3] for r in res]
    print(f'title = {title} / ids = {ids}')
    return title, img, ids, levels


def recipe_detail(id:int):

    print(f'search food ids = {id}')
    sql_a = """
        SELECT
            i.name as ing_name,
            b.value
        FROM food f JOIN basic_ing b ON b.food_id=f.id
            JOIN ingredients i ON i.id = b.ing_id
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
    
    with connect().cursor() as cur:
        cur.execute(sql_a, {"ids": id})
        basic_ing = cur.fetchall()
        cur.execute(sql_b, {'ids': id})
        recipes = cur.fetchall()
        cur.execute(sql_c, {'ids': id})
        food_res = cur.fetchone()

    # print(basic_ing)
    ingredient = [ing[0] for ing in basic_ing]
    values = [ing[1] for ing in basic_ing]

    # print(recipes)
    steps = [f'{r[0]}단계' for r in recipes]
    text = [r[1] for r in recipes]
    recipe_img = [r[2] for r in recipes]

    print(food_res)

    result = [ingredient, values, steps, text, recipe_img]

    return result, food_res

def kor_class(det_class):

    kr_name = []
    for cls in det_class:
        # print(ing_names[cls])
        for item in ing_names[cls]:
            kr_name.append(item)
    return kr_name