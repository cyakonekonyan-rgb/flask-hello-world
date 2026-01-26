import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)
current_weather = "起動中..."

@app.route('/')
def index():
    photo_path = 'static/photo.jpg'
    # キャッシュ対策と更新時刻取得
    timestamp = os.path.getmtime(photo_path) if os.path.exists(photo_path) else time.time()
    update_time_str = time.strftime('%m/%d %H:%M', time.localtime(timestamp))

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
            /* 注意報（⚠️）がある行を赤く強調する設定 */
            .warning { color: #d32f2f; font-weight: bold; background: #ffebee; padding: 2px 5px; border-radius: 4px; display: inline-block; margin-bottom: 5px; }
            .temp-line { font-weight: bold; color: #0d47a1; }
            img { max-width: 100%; height: auto; border-radius: 10px; border: 3px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
            .update-time { font-size: 0.8rem; color: #666; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>でんすけせんせい：飯詰の様子</h3>
            <div class="weather-box">
                {% for line in weather_lines %}
                    <div class="{% if '⚠️' in line %}warning{% elif '予報' in line %}temp-line{% endif %}">{{ line }}</div>
                {% endfor %}
            </div>
            <div class="update-time">📷 {{ update_time }} 更新</div>
            <img src="/static/photo.jpg?{{ time }}" alt="畑">
        </div>
    </body>
    </html>
    ''', 
    weather_lines=current_weather.split(" | "), 
    time=timestamp, 
    update_time=update_time_str
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
