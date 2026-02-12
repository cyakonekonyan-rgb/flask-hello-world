import os
import time
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 起動時の初期メッセージ
current_weather = "週間天気を受信中..."

# --- 重要：static の絶対パスを固定する ---
STATIC_DIR = os.path.join(app.root_path, "static")
PHOTO_PATH = os.path.join(STATIC_DIR, "photo.jpg")
VIDEO_PATH = os.path.join(STATIC_DIR, "rader_anime.mp4")


@app.route('/')
def index():
    # ブラウザのキャッシュ対策（写真の更新時刻を使う）
    timestamp = os.path.getmtime(PHOTO_PATH) if os.path.exists(PHOTO_PATH) else time.time()

    # 動画が存在するか確認（ログも出す）
    video_exists = os.path.exists(VIDEO_PATH)
    photo_exists = os.path.exists(PHOTO_PATH)

    print("=== INDEX DEBUG ===")
    print("PHOTO_PATH:", PHOTO_PATH, "exists:", photo_exists)
    print("VIDEO_PATH:", VIDEO_PATH, "exists:", video_exists)

    return render_template_string(
        '''
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
                .photo-time-line { color: #455a64; font-weight: bold; font-size: 0.95rem; border-bottom: 1px solid #bbdefb; margin-bottom: 8px; padding-bottom: 4px; display: block; }
                .warning { color: #d32f2f; font-weight: bold; background: #ffebee; padding: 3px 6px; border-radius: 4px; display: block; margin: 4px 0; border: 1px solid #ffcdd2; }
                .weekly-line { border-bottom: 1px dashed #cfd8dc; padding: 2px 0; }
                .weekly-line:last-child { border-bottom: none; }

                .media-content { width: 100%; max-width: 640px; margin: 0 auto; }
                img, video { width: 100%; height: auto; border-radius: 10px; border: 2px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 10px; display: block; }
            </style>
        </head>
        <body>
            <div class="container">
                <h3 style="margin: 10px 0;">でんすけせんせい：飯詰</h3>

                <div class="weather-box">
                    {% for line in weather_lines %}
                        {% if '🕒' in line or '📸' in line %}
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
                        <p style="font-size: 0.7rem; color: #666; margin-bottom: 2px;">▼雨雲レーダー（アニメ）</p>
                        <video controls autoplay loop muted playsinline poster="/static/photo.jpg?{{ time }}">
                            <source src="/static/rader_anime.mp4?{{ time }}" type="video/mp4">
                            このブラウザは video 再生に対応していません
                        </video>
                    {% else %}
                        <p style="font-size: 0.75rem; color: #999; margin: 6px 0;">
                            （動画ファイルがまだありません）
                        </p>
                    {% endif %}

                    <p style="font-size: 0.7rem; color: #666; margin-bottom: 2px;">▼現在の外の様子</p>
                    <img src="/static/photo.jpg?{{ time }}" alt="飯詰の風景">
                </div>
            </div>
        </body>
        </html>
        ''',
        weather_lines=current_weather.split(" | "),
        time=timestamp,
        video_exists=video_exists
    )


@app.route('/upload', methods=['POST'])
def upload_file():
    global current_weather
    os.makedirs(STATIC_DIR, exist_ok=True)

    print("=== UPLOAD DEBUG ===")
    print("STATIC_DIR:", STATIC_DIR)

    # 画像保存
    if 'file' in request.files and request.files['file'].filename:
        request.files['file'].save(PHOTO_PATH)
        print("Saved photo:", PHOTO_PATH, "size:", os.path.getsize(PHOTO_PATH))
    else:
        print("No photo file received")

    # 動画保存
    if 'video' in request.files and request.files['video'].filename:
        # 上書き確実化
        if os.path.exists(VIDEO_PATH):
            os.remove(VIDEO_PATH)
            print("Removed old video:", VIDEO_PATH)

        request.files['video'].save(VIDEO_PATH)
        print("Saved video:", VIDEO_PATH, "size:", os.path.getsize(VIDEO_PATH))
    else:
        print("No video file received")

    current_weather = request.form.get('weather', 'データなし')
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
