import imghdr
from operator import methodcaller
import os
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename

index_dict = {'person': 0, 'bicycle': 1, 'car': 2, 'motorcycle': 3, 'airplane': 4, 'bus': 5, 'train': 6, 'truck': 7,
              'boat': 8, 'traffic light': 9, 'fire hydrant': 10, 'stop sign': 11,
              'parking meter': 12, 'bench': 13, 'bird': 14, 'cat': 15, 'dog': 16, 'horse': 17, 'sheep': 18, 'cow': 19,
              'elephant': 20, 'bear': 21, 'zebra': 22, 'giraffe': 23, 'backpack': 24, 'umbrella': 25,
              'handbag': 26, 'tie': 27, 'suitcase': 28, 'frisbee': 29, 'skis': 30, 'snowboard': 31, 'sports ball': 32,
              'kite': 33, 'baseball bat': 34, 'baseball glove': 35, 'skateboard': 36, 'surfboard': 37,
              'tennis racket': 38, 'bottle': 39, 'wine glass': 40,
              'cup': 41, 'fork': 42, 'knife': 43, 'spoon': 44, 'bowl': 45, 'banana': 46,
              'apple': 47, 'sandwich': 48, 'orange': 49, 'broccoli': 50, 'carrot': 51, 'hot dog': 52, 'pizza': 53,
              'donut': 54,
              'cake': 55, 'chair': 56, 'couch': 57, 'potted plant': 58, 'bed': 59, 'dining table': 60, 'toilet': 61,
              'tv': 62, 'laptop': 63, 'mouse': 64, 'remote': 65, 'keyboard': 66, 'cell phone': 67, 'microwave': 68,
              'oven': 69,
              'toaster': 70, 'sink': 71, 'refrigerator': 72, 'book': 73, 'clock': 74, 'vase': 75, 'scissors': 76,
              'teddy bear': 77, 'hair drier': 78, 'toothbrush': 79}


app = Flask(__name__)

# 업로드 최대 용량 설정 (mBytes)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_EXTENSIONS'] = ['.mp4']
app.config['UPLOAD_PATH'] = 'uploads'
#app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_PATH'] = 'outputs'

#비디오 변경시 필요없음
def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    if os.path.exists(app.config['OUTPUT_PATH']):
        for file in os.scandir(app.config['OUTPUT_PATH']):
            os.remove(file.path)
    files = os.listdir(app.config['UPLOAD_PATH'])
    print(str(files))

    #files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        files = files[-1].replace('%5B', '').replace('%5D', '')
    else: 
        files = ''
    #filename = secure_filename(files)
    
    
    return render_template('index.html', files = str(files), data = index_dict.keys())

@app.route('/', methods=['POST'])
def upload_files():
    
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    #filename = request.files.get('file', False)
    print(str(filename))
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            #or file_ext != validate_image(uploaded_file.stream):
            return "Invalid image", 400
        if os.path.exists(app.config['UPLOAD_PATH']):
            for file in os.scandir(app.config['UPLOAD_PATH']):
                os.remove(file.path)
        
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        #uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    #return '', 204
    #return redirect(url_for('index'))
    #return redirect(url_for('select'))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
    #return redirect(url_for('static', filename='uploads/' + filename), code=301)



@app.route('/result',methods=['GET','POST'])
def output_video():
    search = request.form.get("order")
    print(str(search))
    output = os.listdir(app.config['OUTPUT_PATH'])
    print(str(output))
    if output:
        output = output[-1].replace('%5B', '').replace('%5D', '')
        print(output)
    else: 
        print(2)
        output = ''

    #files = os.listdir(app.config['UPLOAD_FOLDER'])
    if os.path.exists(app.config['UPLOAD_PATH']):
        for file in os.scandir(app.config['UPLOAD_PATH']):
            os.remove(file.path)
    return render_template('result.html', output = output)
    #return redirect(url_for('outputs', output=output))

@app.route('/result1', methods=['POST'])
def output_video1():
    search = request.form.get("order")
    print(str(search))
    return str(search)
@app.route('/display/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	#return redirect(url_for('outputs', filename= filename))
    return send_from_directory(app.config['OUTPUT_PATH'], filename)


if __name__ == '__main__':
    app.run(debug=True)