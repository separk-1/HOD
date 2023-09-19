import os

def count_text_files(path):
    text_file_count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".txt"):
                text_file_count += 1
    return text_file_count

cam_ids = {'D1', 'D2', 'D3', 'D4', 'D8', 'S'}
for cam_id in cam_ids:
    path = f"D:/Dataset/Site_HD/labels/{cam_id}"
    total_text_files = count_text_files(path)
    print(f"경로 '{path}' 내의 텍스트 파일 개수: {total_text_files}개")
