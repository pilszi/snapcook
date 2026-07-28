from fastapi import FastAPI

from static.oracle.db import connect
from src.job.detect_yolo import detect_img
from src.job.search_db import detect_foods, ing_names, recipe_detail

app = FastAPI()


@app.get('/yolo/detection')
def detection(file:str):

    print(f'detection file = {file}')
    det_class = detect_img(file)
    # print(det_class)
    print(f'result class = {det_class}')
    kor_class = [ing_names[x] for x in det_class]

    return kor_class


@app.post('/api/snapcook')
def snapcook(data:dict):

    print(f'snapcook data = {data}')
    res = detect_foods(data['class'])
    
    return res


@app.get('/recipe/detail')
def detail(id:int):
    
    result, food_res = recipe_detail(id)
    print(f'detail_recipe = {food_res}')

    return {'result': result, 'food': food_res}