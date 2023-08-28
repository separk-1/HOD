import shutil
# 원본 txt 파일을 읽기 모드로 열기
with open('file_list.txt', 'r') as f:
    lines = f.readlines()

# 변환된 파일명을 저장할 리스트 생성
new_lines = []

# 각 줄을 새로운 형식으로 변환
for line in lines:
    line = line.strip()  # 줄바꿈 문자 제거
    parts = line.split('_')  # 언더스코어(_)로 문자열을 분리
    new_line = f"{parts[0]}/{parts[0]}_{parts[1]}/{parts[0]}_{parts[1]}_{parts[2]}_{parts[3][0]}.png"  # 새로운 형식으로 조립
    new_lines.append(new_line)  # 리스트에 추가

# 새 txt 파일을 쓰기 모드로 열어 변환된 파일명을 저장
with open('file_list.txt', 'w') as f:
    for new_line in new_lines:
        f.write(f"{new_line}\n")

# 원본 txt 파일을 읽기 모드로 열기
with open('file_list.txt', 'r') as f:
    files = f.read().splitlines()

# 복사할 원본 파일의 기본 경로
source_folder = "D:/Dataset/Site/images/"

# 복사될 대상의 기본 경로
destination_folder = "I:/Dataset_sample/images/"

# 파일 목록을 돌면서 파일 복사하기
for file_path in files:
    source = source_folder + file_path
    file_name = file_path.split("/")[-1]
    destination = destination_folder + file_name

    # 실제 파일 복사 수행
    shutil.copy(source, destination)

print("Files have been copied.")