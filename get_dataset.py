import shutil
import os

# 원본 txt 파일을 읽기 모드로 열기
with open('file_list_modified.txt', 'r') as f:
    files = f.read().splitlines()

# 복사할 원본 파일의 기본 경로
source_folder = "D:/Dataset/Site/images/"

# 복사될 대상의 기본 경로
destination_folder = "I:/Dataset_sample/images/"

# 파일 목록을 돌면서 파일 복사하기
not_found_files = []  # not found된 파일을 저장할 리스트

for file_path in files:
    source = source_folder + file_path
    file_name = file_path.split("/")[-1]
    destination = destination_folder + file_name

    # 대상 경로에 파일이 이미 있는지 확인
    if not os.path.exists(destination):
        try:
            # 실제 파일 복사 수행
            shutil.copy(source, destination)
        except FileNotFoundError:
            print(f"File {file_name} not found. Skipping.")
            not_found_files.append(file_name)

# not found된 파일 목록을 정렬
not_found_files.sort()

# 정렬된 not found된 파일 목록을 txt 파일로 저장
with open('not_found_files.txt', 'w') as f:
    for file_name in not_found_files:
        f.write(f"{file_name}\n")

print("Files have been copied.")
