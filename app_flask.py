import os
import uuid
from flask import Flask, render_template, request, jsonify
import requests



app = Flask(__name__)

url = "http://127.0.0.1:8000"

file_path = "static/upload"

def file_split(filename):
    print(f' ==== {filename} 확장자 분리 ====')
    name = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]
    uu_num = uuid.uuid4().hex[:6]
    file = f'{name}_{uu_num}'
    return file, ext

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template("main.html")


@app.route('/save_img', methods=['POST'])
def snapcook():
    file = request.files['file']
    filename = file.filename
    print(filename)
    name, ext = file_split(filename)
    file.save(f'{file_path}/{name}{ext}')

    return jsonify({"status": "success", "filename": f'{name}{ext}'})


@app.route('/yolo/detection', methods=['POST'])
def yolo_detection():
    file = request.json.get('file')
    # filename = file.filename
    print('='*60)
    print(file)
    response = requests.get(f'{url}/api/yolo/detection?file={file}')
    result = response.json()
    # print(result)

    return jsonify({"detect": result})


@app.route('/detect', methods=['POST'])
def detect():
    cls = request.form.get('cls')
    cls_list = [item.strip() for item in cls.split(',')]
    file = request.form.get('file')
    print(file)
    print('='*60)
    return render_template('detect.html',
                           detect = cls_list,
                           filename = file)


@app.route('/api/snapcook', methods=['POST'])
def api_snapcook():
    data = request.json.get('class')
    response = requests.post(f'{url}/api/snapcook', json={'class': data})
    result = response.json()
    print(f'추천 요리 갯수 : {len(result[0])}')

    return {'result': result}


@app.route('/recipe/detail', methods=['GET'])
def recipe_detail():
    id = request.args.get('id')
    filename = request.args.get('file')
    cls = request.args.get('cls')
    response = requests.get(f'{url}/api/recipe/detail?id={id}')
    result = response.json()
    print('='*60)
    print(result)
    res = result['result']
    food_res = result['food']

    return render_template('detail.html',
                           filename = filename,
                           result = res,
                           food = food_res,
                           cls = cls)

# -------------------  진행 중  ---------------------



if __name__ == "__main__":
    app.run(debug=True)