import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 天気情報を保持する変数（初期値）
current_weather = "自宅PCからのデータを待っています..."

@app.route('/')
def index():
    # 画像の有無を確認し、キャッシュ対策のタイムスタンプを作成
    photo_path = 'static/photo.jpg'
    if os.path.exists(photo_path):
        timestamp = os.path.getmtime(photo_path)
        update_time_str = time.strftime('%m/%d %H:%M', time.localtime(timestamp))
    else:
        timestamp = time.time()
        update_time_str = "---"

    # HTMLテンプレート
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>でんすけせんせい - 飯詰の様子</title>
        <style>
            body { 
                font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif; 
                text-align: center; 
                background-color: #f4f7f9; 
                padding: 10px; 
                color: #333; 
            }
            .container { 
                background: white; 
                padding: 20px; 
                border-radius: 20px; 
                box-shadow: 0 8px 20px rgba(0,0,0,0.1); 
                display: inline-block; 
                max-width: 95%; 
            }
            h1 { color: #2c3e50; margin-bottom: 15px; font-size: 1.4rem; }
            .weather-container {
                background: #e3f2fd;
                padding: 15px;
                border-radius: 12px;
                color: #0d47a1;
                font-size: 1rem;
                margin-bottom: 20px;
                text-align: left;
                line-height: 1.8;
                border: 1px solid #bbdefb;
            }
            .day-line {
                border-bottom: 1px dashed #bbdefb;
                padding: 5px 0;
            }
            .day-line:last-child { border-bottom: none; }
            img { 
                max-width: 100%; 
                height: auto; 
                border-radius: 10px; 
                box-shadow: 0 4px 10px rgba(0,0,0,0.15); 
            }
            .footer { 
                margin-top: 15px; 
                color: #999; 
                font-size: 0.75rem; 
            }
            .update-badge {
                display: inline-block;
                background: #6c757d;
                color: white;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 0.8rem;
                margin-bottom: 10px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>でんすけせんせい：飯詰の畑</h1>
            
            <div class="weather-container">
                {% for line in weather_lines %}
                    <div class="day-line">{{ line }}</div>
                {% endfor %}
            </div>

            <div class="update-badge">カメラ更新: {{ update_time }}</div>
            <br>
            <img src="/static/photo.jpg?{{ time }}" alt="畑の様子" onerror="this.src='https://via.placeholder.com/600x400?text=Wait+for+Upload...'">
            
            <div class="footer">
                青森県五所川原市飯詰より自動配信中
            </div>
        </div>
    </body>
    </html>
    ''', 
    # 天気情報を「 | 」で区切って1行ずつ表示するようにリスト化
    weather_lines=current_weather.split(" | "), 
    time=timestamp, 
    update_time=update_time_str
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    
    # フォルダ作成の確認
    if not os.path.exists('static'):
        os.makedirs('static')

    if 'file' not in request.files:
        return "No file", 400
    
    # 画像の保存
    file = request.files['file']
    file.save(os.path.join('static', 'photo.jpg'))
    
    # 天気情報の保存（今日・明日・明後日の3日分）
    current_weather = request.form.get('weather', 'データなし')
    
    return "Upload successful", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
