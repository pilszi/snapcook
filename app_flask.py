import os
from flask import Flask, render_template, request
import requests



app = Flask(__name__)

url = "http://127.0.0.1:8000"

file_path = "static/upload"

def file_split(filename):
    print(f' ==== {filename} 확장자 분리 ====')
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    return name, ext

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/snapcook', methods=['POST'])
def snapcook():
    file = request.files['file']
    filename = file.filename
    print(filename)
    file.save(f'{file_path}/{filename}')
    name, ext = file_split(filename)

    return render_template('index.html',
                           file = name)


@app.route('/yolo/detection', methods=['GET'])
def yolo_detection():
    filename = request.args.get('file')
    # print(filename)
    response = requests.get(f'{url}/yolo/detection?file={filename}')
    result = response.json()
    # print(result)

    return render_template('detect.html',
                           file = filename,
                           detect = result)


@app.route('/api/snapcook', methods=['POST'])
def api_snapcook():
    req = request.get_json()
    data = req.get('class')
    print('='*60)
    print(data)
    response = requests.post(f'{url}/snapcook', json={'class': data})
    result = response.json()
    print(result)
    return {'result': result}


# -------------------  진행 중  ---------------------

@app.route('/recipe/detail', methods=['GET'])
def recipe_detail():
    id = request.args.get('id')
    
    response = requests.get(f'{url}/recipe/detail?id={id}')
    result = response.json()
    print(result)
    res = result['result']
    food_res = result['food']

    return render_template('detail.html',
                           result = res,
                           food = food_res)




if __name__ == "__main__":
    app.run(debug=True)