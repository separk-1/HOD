import os
import shutil
import subprocess

exp_count = 35

yolo_path = './codes/models/yolov5'
source_path = f'{yolo_path}/runs/train/exp{exp_count}/weights/best.pt'
weight_path = './results/weights/yolov5.pt'
shutil.copy(source_path, weight_path)

# detect.py를 실행합니다.
subprocess.run(['python', f'{yolo_path}/detect.py', '--weights', f'{weight_path}', '--source', './datasets/sample/test/images/*.png', '--device', '0'])

# detect한 결과를 압축합니다.
shutil.make_archive('test_result', 'zip', f'{yolo_path}/runs/detect/exp{exp_count}')
