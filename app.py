import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 天気情報を保持する変数
current_weather = "取得中..."

@app.route('/')
def index():
    # 画像があるかどうかチェック
    photo_path = 'static/photo.jpg'
    if os.path.exists(photo_path):
        # ファイルの更新日時を数値で取得（キャッシュ対策）
        timestamp = os.path.getmtime(photo_path)
    else:
        timestamp = time.time() # なければ現在の時刻

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>でんすけせんせい - 飯詰の様子</title>
        <style>
            body { font-family: sans-serif; text-align: center; background-color: #f0f4f8; padding: 20px; }
            .container { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); display: inline-block; }
            h1 { color: #2c3e50; }
            .weather-box { font-size: 1.2em; color: #007bff; margin-bottom: 20px; font-weight: bold; }
            img { max-width: 100%; height: auto; border-radius: 10px; border: 5px solid #fff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>現在の飯詰の様子</h1>
            <div class="weather-box">予報: {{ weather }}</div>
            <img src="/static/photo.jpg?{{ time }}" alt="畑の様子" onerror="this.src='https://via.placeholder.com/500x300?text=Waiting+for+Photo...'">
            <p style="color: #666; font-size: 0.8em;">※自動で更新されます</p>
        </div>
    </body>
    </html>
    ''', weather=current_weather, time=timestamp)

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    
    # フォルダ作成の徹底
    try:
        if not os.path.exists('static'):
            os.makedirs('static')
    except Exception as e:
        print(f"Folder creation error: {e}")

    if 'file' not in request.files:
        return "No file", 400
    
    file = request.files['file']
    # 上書き保存
    file.save(os.path.join('static', 'photo.jpg'))
    
    # 天気情報の受け取り
    current_weather = request.form.get('weather', 'データなし')
    
    return "Upload successful", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
