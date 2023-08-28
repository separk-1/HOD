import os

def rename_files_in_directory(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):  # 필요한 파일 형식으로 조건을 설정하세요.
            parts = filename.strip().split('_')
            time_part = parts[-2]  # '1069' 부분이 이 위치에 있다고 가정

            hour = int(time_part[:-2])
            minute = int(time_part[-2:])

            if minute >= 60:
                hour += 1
                minute -= 60

            new_time_part = f"{hour:02}{minute:02}"

            new_filename_parts = parts.copy()
            new_filename_parts[-2] = new_time_part
            new_filename = '_'.join(new_filename_parts)

            old_file_path = os.path.join(directory_path, filename)
            new_file_path = os.path.join(directory_path, new_filename)

            os.rename(old_file_path, new_file_path)
            print(f"Renamed {filename} to {new_filename}")

# 경로를 설정하고 함수를 호출하여 파일명 변경을 수행합니다.
directory_path = "D:/Dataset/Site/labels/D1/D1_230103"
rename_files_in_directory(directory_path)
