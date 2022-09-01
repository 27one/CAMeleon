# -*- coding: utf-8 -*-
import imghdr
from operator import methodcaller
import os
from flask import Flask, render_template, request, redirect, url_for, abort,send_from_directory
from werkzeug.utils import secure_filename

from Utils import print_update, convert_frames_to_video
from Inpainting import inpaint_all_frames
from MaskRCNN import generate_masks_from_video
import os
import sys
import argparse
import warnings
from AudioProcessing import get_objs_to_mask, add_audio_to_video
import shutil
#import time
import cv2
def test_fps(videoPath):
    cap = cv2.VideoCapture(videoPath)

    fps = cap.get(cv2.CAP_PROP_FPS)
    return fps
warnings.filterwarnings("ignore", category=Warning)

korean_index_sel = ['사람', '자전거', '자동차', '오토바이', '비행기', '버스', '기차', '트럭', '보트', '신호등', '소화전', '정지 신호', '주차료 징수 기', '벤치', '새', '고양이', '개', '말', '양', '암소', '코끼리', '곰', '얼룩말', '기린', '배낭', '우산', '핸드백', '넥타이', '여행용 가방', '원반', '스키', '스노우 보드', '스포츠 볼', '연', '야구 방망이', '야구 글러브', '스케이트 보드', '서핑 보드', '테니스 라켓', '병', '와인 잔', '컵', '포크', '칼', '숟가락', '그릇', '바나나', '사과', '샌드위치', '오렌지', '브로콜리', '당근', '핫도그', '피자', '도넛', '케이크', '의자', '침상', '화분 식물', '침대', '식탁', '화장실', 'TV', '랩탑', '마우스', '리모콘', '건반', '휴대 전화', '전자레인지', '오븐', '토스터기', '싱크대', '냉장고', '책', '시계', '꽃병', '가위', '테디 베어', '헤어 드라이어', '칫솔']
englisth_index_sel = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
index_sel = {x : y for x, y in zip(korean_index_sel,englisth_index_sel)}
        
parser = argparse.ArgumentParser()
parser.add_argument('--inflation', default=5, type=int,
                    help='Number of pixels to inflate the object mask.')
parser.add_argument('--minConfidence', default=0.5, type=float,
                    help='The minimum confidence MaskRCNN needs to consider an object mask valid.')
args, unknown = parser.parse_known_args()

app = Flask(__name__)

# 업로드 최대 용량 설정 (mBytes)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
#app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_EXTENSIONS'] = ['.mp4']
app.config['UPLOAD_PATH'] = 'uploads'
app.config['OUTPUT_PATH'] = 'output'
#app.config['IMAGE_PATH'] = 'images'

def txt_write(filename):
    with open("file.txt", "w") as f:
        f.write(filename)

def txt_read():
    with open('file.txt', 'rb') as f:
        filename = f.readline()
    return filename.decode('utf-8')

def video_remove(video_path):
    if os.path.exists(video_path):
        for file in os.scandir(video_path):
            os.remove(file.path)

@app.errorhandler(413)
def too_large(e):
    return "File is too large", 413

@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    #print(str(files))
    if files:
        files = files[-1].replace('%5B', '').replace('%5D', '')
    else: 
        files = ''
    return render_template('index.html', files = str(files), data = korean_index_sel)

@app.route('/', methods=['POST'])
def upload_files():
    #video_remove(app.config['OUTPUT_PATH'])
    #if os.path.exists(filePath):
        #shutil.rmtree(filePath)
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)

    txt_write(filename)

    print(str(filename))
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] :
            #or file_ext != validate_image(uploaded_file.stream):
            return "Invalid mp4 video", 400
        video_remove(app.config['UPLOAD_PATH'])
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        
    #return '', 204
    #return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)
    #return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/result',methods=['GET','POST'])
def output_video():
    filename = txt_read()
    videoPath = 'uploads/' + filename
    minConfidence = args.minConfidence
    inflation = args.inflation
    #print(filename)
    search = request.form.get("order")
    #print(str(search))

    if not os.path.exists(videoPath):
        sys.exit("Could not locate video '" + videoPath + "'")

    #objectsToMask = get_objs_to_mask(videoPath, index_sel[search])

    print("Masking objects from the video...")
    #fps = generate_masks_from_video(videoPath, objectsToMask, minConfidence, inflation)
    #Masking 생략 하고 Inpainting 진행하기 위한 fps 설정
    fps = test_fps(videoPath)

    print("Masking completed. Painting out masked objects...")
    #inpaint_all_frames(videoPath)

    print("Inpainting completed. Compiling to video...")
    compiledPath = convert_frames_to_video(videoPath, fps)
    add_audio_to_video(compiledPath, fps)
    #remove soundless video
    #os.remove(compiledPath)

    print("Compiled! to " + compiledPath[:-3] + 'mp4')

    output = (compiledPath[:-3] + 'mp4').replace('output/', '')
    print(str(output))

    #video_remove(app.config['UPLOAD_PATH'])
    
    return render_template('result.html', output = output)
    #return redirect(url_for('outputs', output=output))

@app.route('/output/<filename>')
def display_video(filename):
	#print('display_video filename: ' + filename)
	#return redirect(url_for('outputs', filename= filename))
    return send_from_directory(app.config['OUTPUT_PATH'], filename)

if __name__ == '__main__':
    try:
        os.mkdir('output/')
        os.mkdir('uploads/')
    except Exception:
        pass
    app.run(debug=True)