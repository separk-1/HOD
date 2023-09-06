import os
import shutil
import random

# 원본 데이터셋 폴더 경로
images_folder = '../../datasets/sample/train/images'
labels_folder = '../../datasets/sample/train/labels'

# 새로 생성할 폴더 경로
images_test_folder = '../../datasets/sample/test/images'
labels_test_folder = '../../datasets/sample/test/labels'

# 새 폴더 생성 (이미 존재한다면 덮어쓰기)
os.makedirs(images_test_folder, exist_ok=True)
os.makedirs(labels_test_folder, exist_ok=True)

# 파일 리스트 불러오기 (.png와 .txt 파일만)
image_files = [f for f in os.listdir(images_folder) if f.endswith('.png')]
label_files = [f for f in os.listdir(labels_folder) if f.endswith('.txt')]

# 파일 이름의 기본 부분만 사용하여 리스트 생성
image_files_base = [os.path.splitext(f)[0] for f in image_files]
label_files_base = [os.path.splitext(f)[0] for f in label_files]

# 일치하는 파일만 남기기
matching_files_base = set(image_files_base).intersection(label_files_base)

# 리스트로 변환하고 섞기
matching_files_base = list(matching_files_base)
random.seed(42)  # 재현 가능성을 위한 시드 설정
random.shuffle(matching_files_base)

# 9:1 비율로 나누기
num_files = len(matching_files_base)
num_train = int(0.7 * num_files)
train_files_base = matching_files_base[:num_train]
val_files_base = matching_files_base[num_train:]

# 파일을 새로운 폴더로 복사
for f_base in train_files_base:
    shutil.move(os.path.join(images_folder, f_base + '.png'), os.path.join(images_test_folder, f_base + '.png'))
    shutil.move(os.path.join(labels_folder, f_base + '.txt'), os.path.join(labels_test_folder, f_base + '.txt'))
