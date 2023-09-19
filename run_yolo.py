import os
import shutil
import subprocess

epoch = 1000


yolo_path = './codes/models/yolov5'

# comet_ml을 설치합니다.
subprocess.run(['pip', 'install', 'comet_ml'])

# 필요한 라이브러리를 설치합니다.
subprocess.run(['pip', 'install', '-qr', f'{yolo_path}/requirements.txt'])

# train.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/train.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--epochs', f'{epoch}', '--device', '0'])

# training 결과를 압축합니다.
shutil.make_archive('train_result', 'zip', f'{yolo_path}/runs/train/exp35')

# val.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/val.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--weights', f'{yolo_path}/runs/train/exp35/weights/best.pt', '--device', '0'])
