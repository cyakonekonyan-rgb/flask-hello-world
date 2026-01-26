# --- Render側の app.py 抜粋 ---
from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
# 天気を保存する一時的な変数
current_weather = "取得中..."

@app.route('/')
def index():
    # HTMLの中に天気を表示する場所を作る
    return render_template_string('''
    <h1>現在の飯詰の様子</h1>
    <p style="font-size: 20px; color: blue;">予報: {{ weather }}</p>
    <img src="/static/photo.jpg" style="width:500px;">
    ''', weather=current_weather)

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    if 'file' not in request.files:
        return "No file", 400
    
    # 画像の保存
    file = request.files['file']
    file.save('static/photo.jpg')
    
    # 天気情報の保存
    current_weather = request.form.get('weather', 'データなし')
    
    return "OK", 200
