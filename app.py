import datetime
import logging as rel_log
import os
import shutil
from datetime import timedelta
from flask import *
from processor.AIDetector_pytorch import Detector

import core.main
from paddleOcr import orc_draw_orc
from ddddOrc import ocr_code

UPLOAD_FOLDER = r'./uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg'])
app = Flask(__name__)
app.secret_key = 'secret!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

werkzeug_logger = rel_log.getLogger('werkzeug')
werkzeug_logger.setLevel(rel_log.ERROR)

# 解决缓存刷新问题
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)

c_model = {}
file_list = os.listdir('weights/')
for file in file_list:
    name = os.path.splitext(file)[0]
    c_model[name] = Detector(file)

# 添加header解决跨域
@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    return response


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return redirect(url_for('static', filename='./index.html'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    file = request.files['file']
    name = request.form['name']
    m = 'weights/'+name+'.pt'
    if not os.path.exists(m):
        return jsonify({'status': 0, 'msg': '模型不存在'})
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        pid, image_info = core.main.c_main(
            src_path, c_model[name], file.filename.rsplit('.', 1)[1])
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        url = '/tmp/draw/' + str(year) + '/' + str(month) + '/'
        return jsonify({'status': 1,
                        'draw_url': url + pid,
                        'image_info': image_info})

    return jsonify({'status': 0})


@app.route('/orc/upload', methods=['GET', 'POST'])
def orc_upload_file():
    file = request.files['file']
    lang = request.form['lang']
    if lang is None:
        lang = 'ch'
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(src_path)
        res = orc_draw_orc(src_path, lang)
        return jsonify({'status': 1,
                        'draw_url': 'uploads/'+file.filename,
                        'image_info': res})

    return jsonify({'status': 0})

@app.route('/codeOrc/upload', methods=['GET', 'POST'])
def orc_code_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        src_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        print(src_path)
        file.save(src_path)
        res = ocr_code(src_path)
        return jsonify({'status': 1,
                        'info': res})

    return jsonify({'status': 0})

@app.route("/download", methods=['GET'])
def download_file():
    # 需要知道2个参数, 第1个参数是本地目录的path, 第2个参数是文件名(带扩展名)
    return send_from_directory('data', 'testfile.zip', as_attachment=True)



# show photo
@app.route('/tmp/<path:file>', methods=['GET'])
def show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'tmp/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


# show photo
@app.route('/uploads/<path:file>', methods=['GET'])
def u_show_photo(file):
    if request.method == 'GET':
        if not file is None:
            image_data = open(f'uploads/{file}', "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response


if __name__ == '__main__':
    files = [
        'uploads', 'tmp/ct', 'tmp/draw',
        'tmp/image', 'tmp/mask', 'tmp/uploads'
    ]
    for ff in files:
        if not os.path.exists(ff):
            os.makedirs(ff)

    app.run(host='127.0.0.1', port=5003, debug=False)
