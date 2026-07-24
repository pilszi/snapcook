from static.oracle.db import connect

ing_names = None

try:
    cur = connect().cursor()
    cur.execute("""SELECT i.name, ig.en_name FROM ing_name ig JOIN ingredients i ON i.id = ig.ing_id""")
    ing_res = cur.fetchall()
    ing_names = {res[1]: res[0] for res in ing_res}
    cur.close()
    print(ing_names)
except Exception as e:
    print(e)


def detect_foods(cls):

    count_target = len(cls) # 2개
    bind_names = ', '.join(f":{i}" for i in range(count_target))

    sql_b = f"""
    SELECT 
        name, image, id
    FROM food
        WHERE id IN (
            SELECT b.food_id
            FROM basic_ingredients b JOIN ingredients i ON i.id=b.ingredient_id
                JOIN food f ON f.id = b.food_id
                WHERE i.name IN ({bind_names})
                GROUP BY b.food_id
                HAVING MAX(CASE WHEN f.name LIKE '%' || i.name || '%' THEN 1 ELSE 0 END) = 1
        )
    """
    with connect().cursor() as cur:
        cur.execute(sql_b, cls)   
        res = cur.fetchall()
    title = [r[0] for r in res]
    img = [r[1] for r in res]
    ids = [r[2] for r in res]
    
    return title, img, ids