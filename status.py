import os
from datetime import datetime
from colorama import init, Fore


def extract_date(date_string):
    """날짜 형식 변환: 230109 -> 23년 1/9(요일)"""
    month = int(date_string[-4:-2])
    day = int(date_string[-2:])
    year = 2000 + int(date_string[:-4])

    date_obj = datetime(year, month, day)
    weekdays_kr = ["월", "화", "수", "목", "금", "토", "일"]
    weekday = weekdays_kr[date_obj.weekday()]

    return f"{year-2000}년 {month}/{day}({weekday})"

def count_files_in_directory(path):
    if not os.path.exists(path):
        print("지정된 경로가 존재하지 않습니다.")
        return

    if not os.path.isdir(path):
        print("지정된 경로는 디렉토리가 아닙니다.")
        return

    folder_dict = {}

    for foldername, subfolders, filenames in os.walk(path):
        parts = foldername.split(os.path.sep)
        
        if len(parts) >= 3:  # 'D' 폴더와 '날짜' 폴더가 모두 포함된 경로를 대상으로 함
            main_folder = parts[-2]
            date_folder = parts[-1]

            if main_folder.startswith("D") and date_folder.isdigit():
                if main_folder not in folder_dict:
                    folder_dict[main_folder] = []
                folder_dict[main_folder].append((extract_date(date_folder), len(filenames)))

        # 폴더별 정보 출력
    for main_folder in sorted(folder_dict.keys()):
        dates = sorted(folder_dict[main_folder], key=lambda x: x[0])
        
        # Dx 폴더의 하위 폴더 개수 계산
        subfolder_count = len(dates)
        percentage = subfolder_count / 208 * 100

        color = Fore.RESET
        print(f"{color}{main_folder}({percentage:.2f}%)")
        
        for date, count in dates:
            # 데이터 개수에 따른 색상 설정
            if count > 800:
                color = Fore.GREEN
            elif 500 <= count <= 800:
                color = Fore.BLUE
            elif 0 <= count <= 500:
                color = Fore.RED
            else:
                color = Fore.RESET
            
            print(f"{color}- {date}: {count}")
        
        print()

if __name__ == "__main__":
    directory_path = "G:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/output"
    count_files_in_directory(directory_path)
