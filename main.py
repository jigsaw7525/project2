from flask import Flask, render_template, request
from datetime import datetime
from pm25 import *
import json

# 產生flask物件
app = Flask(__name__)



# 3.現在時間
@app.route('/today')
def time():
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return date


# PM2.5區域

# 分析PM2.5之資訊
@app.route('/pm25-data', methods=["GET", "POST"])
def get_pm25_data():
    # import pm25.py的get_pm25()
    columns, values = get_pm25()

    site = [value[1] for value in values]
    pm25 = [value[2] for value in values]
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    datas = [[value[1], value[-1]]for value in values]
    datas = sorted(datas, key=lambda x: x[-1])

    data = {'site': site, 'pm25': pm25, 'date': date,
            'highest': datas[-1], 'lowest': datas[0]}
    print(data)
    return json.dumps(data, ensure_ascii=False)

# PM2.5表格
@app.route('/pm25', methods=["GET", "POST"])
def pm25():

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    columns, values = get_pm25()

    if request.method == 'GET':
        columns, values = get_pm25()

    if request.method == 'POST':
        if request.form.get('reverse'):
            columns, values = get_pm25(type=1)
        elif request.form.get('ascending'):
            columns, values = get_pm25(type=2)

    return render_template("./pm25.html", columns=columns, values=values, date=date)

# 全台PM2.5圖表
@app.route('/')
def pm25_chart():
    countys = get_county()
    return render_template('./pm25-charts-bulma.html', countys=countys)

# 六都PM2.5圖表
@app.route('/six-data', methods=["GET", "POST"])
def get_six_json():
    datas = get_six_pm25()
    return json. dumps({'county': list(datas.keys()), 'pm25': list(datas.values())},
                       ensure_ascii=False)

# 各鄉鎮市區PM2.5圖表
@app.route('/county-pm25/<string:county>', methods=["GET", "POST"])
def get_county_json(county):
    datas = get_county_pm25(county)
    data = {
        'title': county,
        'county': [data[0] for data in datas],
        'pm25': [data[-1] for data in datas]
    }
    return json.dumps(data, ensure_ascii=False)


# 啟動
if __name__ == "__main__":
    #debug = True (儲存後自動更新)
    app.run(debug=True)
