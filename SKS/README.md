
# Jetson	nano에서 실행하기
• PyTorch 1.8.0 다운로드 및 dependency	설치

%	wget https://nvidia.box.com/shared/static/p57jwntv436lfrd78inwl7iml6p13fzh.whl -O	torch- 1.8.0-cp36-cp36m-linux_aarch64.whl

%	sudo apt-get	install	python3-pip	libopenblas-base	libopenmpi-dev

• Cython,	numpy, PyTorch 설치

%	pip3	install	Cython

%	pip3	install	numpy torch-1.8.0-cp36-cp36m-linux_aarch64.whl

• torchvision dependency	설치

%	sudo apt-get	install	libjpeg-dev	zlib1g-dev	libpython3-dev	libavcodec-dev	libavformat-dev	libswscale-dev

%	git	clone	--branch	v0.9.0	https://github.com/pytorch/vision torchvision

%	cd	torchvision

%	export	BUILD_VERSION=0.9.0

%	python3	setup.py install	--user

# YOLO	v5	설치
• YOLOv5	공식 레포지토리 복사

%	git	clone	https://github.com/ultralytics/yolov5

%	cd	yolov5

• requirements.txt 에서 다음 내용 제거

%	numpy>=1.18.5

%	opencv-python>=4.1.2

%	torch>=1.7.0

%	torchvision>=0.8.1

• requirements.txt 설치

%	python3	-m	pip	install	--upgrade	pip

%	python3	-m	pip	install	-r	requirements.txt
