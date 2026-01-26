import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 天気情報を保持する変数
current_weather = "取得中..."

# 1. ブラウザで見た時の画面（トップページ）
@app.route('/')
def index():
    # シンプルなHTMLで画像と天気を表示
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
            <img src="/static/photo.jpg?{{ time }}" alt="畑の様子">
            <p style="color: #666; font-size: 0.8em;">※自動で10分おきに更新されます</p>
        </div>
    </body>
    </html>
    ''', weather=current_weather, time=os.path.getmtime('static/photo.jpg') if os.path.exists('static/photo.jpg') else 0)

# 2. 自宅PCからのアップロードを受け取る窓口
@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    
    # 保存先フォルダ（static）がなければ作成
    UPLOAD_FOLDER = 'static'
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # 送られてきたファイルの確認
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    # 画像を static/photo.jpg として保存（上書き）
    file.save(os.path.join(UPLOAD_FOLDER, 'photo.jpg'))
    
    # 同時に送られてきた天気テキストを受け取る（なければ「データなし」）
    current_weather = request.form.get('weather', 'データなし')
    
    print(f"Update received: Weather={current_weather}")
    return "Upload successful", 200

if __name__ == "__main__":
    # Renderのポート番号に対応
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
