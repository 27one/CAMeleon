# SKT FlyAi 4

코드 및 자료 공유 용도

팀프로젝트 주의점

1. 자신의 폴더만 사용하기 : 타인의 자료는 복사해서 자신의 폴더에서 사용
2. git pull 이후 git push하기 (백업 문제 주의)
3. 가능하면 README에서 설명해주기
4. 업데이트할 때는 폴더에 따라 버전 나누기(백업용)

## Installation
이 프로젝트를 clone하고 새 Conda 환경 구축한 뒤, 아래 코드를 실행
```
$ conda create <가상환경이름> python=3.6
```
```
$ conda activate <가상환경이름>
```
''`
$ git clone 
'''
프로젝트가 위치하는 디렉토리로 이동하여 아래 코드를 실행
```
pip install mxnet==1.7.0.post2
pip install tensorflow==1.7.1
pip install gluoncv==0.4.0
pip install git+https://github.com/JiahuiYu/neuralgym
pip install opencv-python==4.5.1.48
pip install natsort==7.1.1
pip install moviepy==1.0.3
pip install speechRecognition==3.8.1
```
마지막으로, [이 드라이브](https://drive.google.com/drive/folders/1y7Irxm3HSHGvp546hZdAZwuNmhLUVcjO)의 *snap-0.meta*와 *snap-0.data-00000-of-00001*을 **model_logs\release_places2_256**폴더로 다운로드

## Usage
구축한 Conda환경에 접속하여 프로젝트가 존재하는 디렉토리로 경로를 맞춰준 뒤, 아래 코드를 실행
```
python app.py
```
그리고 http://127.0.0.1:5000/ 으로 접속하면 서비스 이용 가능
