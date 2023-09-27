import os
import subprocess

epoch = 3

yolo_path = './codes/models/yolov5'

# train.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/train.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--epochs', f'{epoch}', '--device', '0'])

save_DIR = 'codes/models/yolov5/runs/train'
subdirectories = [f for f in os.listdir(save_DIR) if os.path.isdir(os.path.join(save_DIR, f))]
subdirectories.sort()
latest_folder = subdirectories[-1]

# val.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/val.py', '--data', f'{yolo_path}/data/custom_dataset.yaml', '--weights', f'{yolo_path}/runs/train/{latest_folder}/weights/best.pt', '--device', '0'])
