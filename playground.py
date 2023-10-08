import os
import glob

# 이미지 파일 확장자 리스트
image_extensions = ["png"]

# 경로 설정 (원하는 경로로 변경하세요)
path_to_search = "F:Dataset/Site_HD/images/D4"

# 이미지 파일 개수를 저장할 변수 초기화
total_image_count = 0

# 디렉토리와 하위 디렉토리에서 이미지 파일 찾기
for root, dirs, files in os.walk(path_to_search):
    # "S_230303" 이후의 폴더는 무시
    if "230320" in root:
        break
    for file in files:
        if file.lower().split(".")[-1] in image_extensions:
            total_image_count += 1

# 이미지 파일 개수 출력
print(f"경로 '{path_to_search}' 내의 이미지 파일 개수: {total_image_count}개")


label_extensions = ["txt"]

# 경로 설정 (원하는 경로로 변경하세요)
path_to_search = "F:Dataset/Site_HD/labels/S"

# 이미지 파일 개수를 저장할 변수 초기화
total_label_count = 0

# 디렉토리와 하위 디렉토리에서 이미지 파일 찾기
for root, dirs, files in os.walk(path_to_search):
    for file in files:
        if file.lower().split(".")[-1] in label_extensions:
            total_label_count += 1

# 이미지 파일 개수 출력
print(f"경로 '{path_to_search}' 내의 텍스트 파일 개수: {total_label_count}개")

total_point = (total_image_count-total_label_count) + 40*total_label_count

print(f"최종 금액: {total_point}원")



