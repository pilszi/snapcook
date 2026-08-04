from fastapi import FastAPI

from static.oracle.db import connect
from src.job.detect_yolo import detect_img
from src.job.search_db import detect_foods, ing_names, recipe_detail, kor_class

app = FastAPI()


@app.get('/api/yolo/detection')
def detection(file:str):

    print(f'detection file = {file}')
    det_class = detect_img(file)
    # print(det_class)
    print(f'result class = {det_class}')
    kr_name = kor_class(det_class)

    return kr_name


@app.post('/api/snapcook')
def snapcook(data:dict):

    print(f'snapcook data = {data}')
    res = detect_foods(data['class'])
    
    return res


@app.get('/api/recipe/detail')
def detail(id:int):
    
    result, food_res = recipe_detail(id)
    print(f'detail_recipe = {food_res}')

    return {'result': result, 'food': food_res}