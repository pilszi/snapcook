from flask import Flask, render_template, request
import requests

app = Flask(__name__)

url = "http://127.0.0.1:8000"

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/snapcook', methods=['GET'])
def snapcook():
    ing = request.args.get('ing', '')

    response = requests.get(f'{url}/snapcook?ing={ing}')
    result = response.json()
    # print(result)
    res = result['result']
    ing_kr = result['ing']

    return render_template('index.html',
                           result = res,
                           ing = ing_kr
                           )


@app.route('/recipe/detail', methods=['GET'])
def recipe_detail():
    ids = request.args.get('ids')
    
    response = requests.get(f'{url}/recipe/detail?id={ids}')
    result = response.json()
    print(result)
    res = result['result']
    food_res = result['food']

    return render_template('detail.html',
                           result = res,
                           food = food_res)




if __name__ == "__main__":
    app.run(debug=True)