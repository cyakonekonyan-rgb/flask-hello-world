import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)
# 起動時の初期メッセージ
current_weather = "週間天気を受信中..."

@app.route('/')
def index():
    photo_path = 'static/photo.jpg'
    # ブラウザのキャッシュ対策
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
            .container { background: white; padding: 15px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); display: inline-block; max-width: 98%; }
            .weather-box { 
                background: #e3f2fd; 
                padding: 12px; 
                border-radius: 12px; 
                text-align: left; 
                font-size: 0.85rem; 
                line-height: 1.5; 
                margin-bottom: 15px; 
                border-left: 5px solid #2196f3; 
            }
            /* 撮影時刻のデザイン */
            .photo-time-line { color: #455a64; font-weight: bold; font-size: 0.95rem; border-bottom: 1px solid #bbdefb; margin-bottom: 8px; padding-bottom: 4px; display: block; }
            /* 注意報の強調表示 */
            .warning { color: #d32f2f; font-weight: bold; background: #ffebee; padding: 3px 6px; border-radius: 4px; display: block; margin: 4px 0; border: 1px solid #ffcdd2; }
            /* 各日の予報の区切り線 */
            .weekly-line { border-bottom: 1px dashed #cfd8dc; padding: 2px 0; }
            .weekly-line:last-child { border-bottom: none; }
            img { max-width: 100%; height: auto; border-radius: 10px; border: 2px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        </style>
    </head>
    <body>
        <div class="container">
            <h3 style="margin: 10px 0;">でんすけせんせい：飯詰</h3>
            <div class="weather-box">
                {% for line in weather_lines %}
                    {% if '📸' in line %}
                        <div class="photo-time-line">{{ line }}</div>
                    {% elif '⚠️' in line and 'なし' not in line %}
                        <div class="warning">{{ line }}</div>
                    {% else %}
                        <div class="weekly-line">{{ line }}</div>
                    {% endif %}
                {% endfor %}
            </div>
            {# ここから不要な「更新」行を削除済み #}
            <img src="/static/photo.jpg?{{ time }}" alt="飯詰の風景">
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
    if 'file' in request.files:
        request.files['file'].save(os.path.join('static', 'photo.jpg'))
    current_weather = request.form.get('weather', 'データなし')
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
