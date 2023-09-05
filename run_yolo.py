import os
import shutil
import subprocess

yolo_path = './codes/models/yolov5'

# comet_ml을 설치합니다 (선택적).
subprocess.run(['pip', 'install', 'comet_ml'])

# 필요한 라이브러리를 설치합니다.
subprocess.run(['pip', 'install', '-qr', f'{yolo_path}/requirements.txt'])

# train.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/train.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--epochs', '10', '--device', '0'])

# training 결과를 압축합니다.
shutil.make_archive('train_result', 'zip', f'{yolo_path}/runs/train/exp')

# val.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/val.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--weights', f'{yolo_path}/runs/train/exp/weights/best.pt', '--device', '0'])

# 모델의 가중치를 다른 경로에 복사합니다.
source_path = f'{yolo_path}/runs/train/exp/weights/best.pt'
target_path = './results/yolov5.pt'
shutil.copy(source_path, target_path)

# detect.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/detect.py', '--weights', f'{yolo_path}/runs/train/exp/weights/best.pt', '--source', './datasets/sample/images_test/*.png', '--device', '0'])

# detect한 결과를 압축합니다.
shutil.make_archive('test_result', 'zip', f'{yolo_path}/runs/detect/exp')
