import os

# 경로 설정
labels_directory = './datasets/D1/labels'  # labels 폴더 경로
images_directory = './datasets/D1/images'  # images 폴더 경로

# labels 폴더 내의 txt 파일 목록을 가져옴
txt_files = [f for f in os.listdir(labels_directory) if f.endswith('.txt')]

# 이미지 파일 이름 목록을 가져옴
image_files = [f for f in os.listdir(images_directory) if f.endswith('.jpg')]

# 이미지 파일 이름 목록을 집합(set)으로 변환하여 검색 속도 향상
image_set = set(image_files)

# labels 폴더 내의 txt 파일을 순회하며 해당 쌍이 존재하는지 확인하고 없는 경우 삭제
for txt_file in txt_files:
    image_name = txt_file.replace('.txt', '.jpg')
    if image_name not in image_set:
        txt_path = os.path.join(labels_directory, txt_file)
        os.remove(txt_path)
        print(f"Removed {txt_file} as corresponding image was not found.")
    else:
        image_path = os.path.join(images_directory, image_name)
        if not os.path.exists(image_path):
            txt_path = os.path.join(labels_directory, txt_file)
            os.remove(txt_path)
            print(f"Removed {txt_file} and {image_name} as the pair was not complete.")
