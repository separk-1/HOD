import os
import subprocess
from datetime import datetime

# 현재 시간을 가져오기
now = datetime.now()

yolo_path = './codes/models/yolov5'

# 문자열 형식 지정
timestamp = now.strftime("%y%m%d_%H%M%S")


save_DIR = 'codes/models/yolov5/runs/train'
subdirectories = [f for f in os.listdir(save_DIR) if os.path.isdir(os.path.join(save_DIR, f))]
subdirectories.sort()
latest_folder = subdirectories[-1]

# val.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/val.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--weights', f'{yolo_path}/runs/train/{latest_folder}/weights/best.pt', '--device', '0'])
