from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# 画像を保存するディレクトリ
UPLOAD_FOLDER = 'static'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    # ブラウザでアクセスした時に画像を表示する
    return '''
    <h1>現在の畑の様子</h1>
    <img src="/static/photo.jpg" style="width:500px;">
    <p>更新時間: 自動で最新の画像が表示されます</p>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    # 自宅PCから送られてきた画像を保存する
    if 'file' not in request.files:
        return "ファイルがありません", 400
    file = request.files['file']
    file.save(os.path.join(UPLOAD_FOLDER, 'photo.jpg'))
    return "アップロード成功", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
