import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)
# 起動時の初期メッセージ
current_weather = "起動中..."

@app.route('/')
def index():
    photo_path = 'static/photo.jpg'
    # ブラウザのキャッシュ対策（画像のURLに付与するタイムスタンプ）
    # ファイルが存在すればその更新日時、なければ現在の時刻を使用
    timestamp = os.path.getmtime(photo_path) if os.path.exists(photo_path) else time.time()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>でんすけせんせい - 飯詰</title>
        <style>
            body { font-family: sans-serif; text-align: center; background-color: #f0f4f8; padding: 10px; color: #333; }
            .container { background: white; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; max-width: 95%; }
            .weather-box { 
                background: #e3f2fd; 
                padding: 15px; 
                border-radius: 12px; 
                text-align: left; 
                font-size: 0.95rem; 
                line-height: 1.7; 
                margin-bottom: 15px; 
                border-left: 5px solid #2196f3; 
            }
            /* 注意報（⚠️）や撮影時刻がある行を強調する設定 */
            .warning { color: #d32f2f; font-weight: bold; background: #ffebee; padding: 2px 5px; border-radius: 4px; display: inline-block; margin-bottom: 5px; }
            .photo-time-line { color: #455a64; font-weight: bold; font-size: 1rem; border-bottom: 1px solid #bbdefb; margin-bottom: 8px; padding-bottom: 4px; display: block; }
            .temp-line { font-weight: bold; color: #0d47a1; }
            img { max-width: 100%; height: auto; border-radius: 10px; border: 3px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>でんすけせんせい：飯詰の様子</h3>
            <div class="weather-box">
                {% for line in weather_lines %}
                    {# '📸'が含まれる行（撮影時刻）や注意報の行の見た目を切り替える #}
                    <div class="{% if '📸' in line %}photo-time-line{% elif '⚠️' in line %}warning{% elif '予報' in line %}temp-line{% endif %}">
                        {{ line }}
                    </div>
                {% endfor %}
            </div>
            {# ここにあった「XX/XX 更新」の1行を削除しました #}
            <img src="/static/photo.jpg?{{ time }}" alt="畑">
        </div>
    </body>
    </html>
    ''', 
    weather_lines=current_weather.split(" | "), 
    time=timestamp
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    if not os.path.exists('static'): os.makedirs('static')
    
    # 画像ファイルの保存
    if 'file' in request.files:
        request.files['file'].save(os.path.join('static', 'photo.jpg'))
    
    # 送信されてきた天気・時刻情報を保存
    current_weather = request.form.get('weather', 'データなし')
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
