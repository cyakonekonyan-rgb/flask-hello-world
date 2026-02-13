import os
import time
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 起動時の初期メッセージ
current_weather = "週間天気を受信中..."
radar_title = "雨雲レーダー（アニメ）"  # デフォルトタイトル

@app.route('/')
def index():
    photo_path = 'static/photo.jpg'
    video_path = 'static/rader_anime.mp4'
    
    # ブラウザキャッシュ対策
    timestamp = os.path.getmtime(photo_path) if os.path.exists(photo_path) else time.time()
    
    # 動画存在確認
    video_exists = os.path.exists(video_path)

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>五所川原市の気象情報</title>
        <style>
            body { 
                font-family: sans-serif; 
                text-align: center; 
                background-color: #f0f4f8; 
                padding: 10px; 
                color: #333; 
            }

            .container { 
                background: white; 
                padding: 15px; 
                border-radius: 20px; 
                box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                display: inline-block; 
                max-width: 98%; 
            }

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

            .photo-time-line { 
                color: #455a64; 
                font-weight: bold; 
                font-size: 0.95rem; 
                border-bottom: 1px solid #bbdefb; 
                margin-bottom: 8px; 
                padding-bottom: 4px; 
                display: block; 
            }

            .warning { 
                color: #d32f2f; 
                font-weight: bold; 
                background: #ffebee; 
                padding: 3px 6px; 
                border-radius: 4px; 
                display: block; 
                margin: 4px 0; 
                border: 1px solid #ffcdd2; 
            }

            .weekly-line { 
                border-bottom: 1px dashed #cfd8dc; 
                padding: 2px 0; 
            }

            .weekly-line:last-child { 
                border-bottom: none; 
            }

            .media-content { 
                width: 100%; 
                max-width: 640px; 
                margin: 0 auto; 
            }

            img, video { 
                width: 100%; 
                height: auto; 
                border-radius: 10px; 
                border: 2px solid #fff; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); 
                margin-bottom: 10px; 
                display: block; 
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h3 style="margin: 10px 0;">
                五所川原市の気象情報
            </h3>

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
            
            <div class="media-content">

                {% if video_exists %}
                    <p style="font-size: 0.7rem; color: #666; margin-bottom: 2px;">
                        ▼{{ radar_title }}
                    </p>

                    <!-- ✅ poster 削除：写真が表示されない -->
                    <video controls autoplay loop muted playsinline>
                        <source src="/static/rader_anime.mp4?{{ time }}" type="video/mp4">
                    </video>
                {% endif %}

                <p style="font-size: 0.7rem; color: #666; margin-bottom: 2px;">
                    ▼現在の外の様子
                </p>

                <img src="/static/photo.jpg?{{ time }}" alt="飯詰の風景">

            </div>
        </div>
    </body>
    </html>
    ''', 
    weather_lines=current_weather.split(" | "), 
    time=timestamp,
    video_exists=video_exists,
    radar_title=radar_title
    )

@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather, radar_title
    
    if not os.path.exists('static'):
        os.makedirs('static')
    
    if 'file' in request.files:
        request.files['file'].save(os.path.join('static', 'photo.jpg'))
    
    if 'video' in request.files:
        v_path = os.path.join('static', 'rader_anime.mp4')
        if os.path.exists(v_path):
            os.remove(v_path)
        request.files['video'].save(v_path)

    current_weather = request.form.get('weather', 'データなし')
    
    # 雨雲レーダータイトルを受信（クライアントから送られた場合）
    received_radar_title = request.form.get('radar_title')
    if received_radar_title:
        radar_title = received_radar_title
        print(f"雨雲レーダータイトル更新: {radar_title}")
    
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
