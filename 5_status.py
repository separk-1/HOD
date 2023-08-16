import os
from datetime import datetime
from colorama import init, Fore
import argparse

def extract_date(date_string):
    """날짜 형식 변환: 230109 -> 23년 1/9(요일)"""
    month = int(date_string[-4:-2])
    day = int(date_string[-2:])
    year = 2000 + int(date_string[:-4])

    date_obj = datetime(year, month, day)
    weekdays_kr = ["월", "화", "수", "목", "금", "토", "일"]
    weekday = weekdays_kr[date_obj.weekday()]

    # formatted_date와 date_obj를 모두 반환합니다.
    return f"{year-2000}년 {month}/{day}({weekday})", date_obj

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
        
        if len(parts) >= 3:
            main_folder = parts[-2]
            date_folder = parts[-1]

            if main_folder.startswith("D") and date_folder.isdigit():
                if main_folder not in folder_dict:
                    folder_dict[main_folder] = []
                formatted_date, date_obj = extract_date(date_folder)
                folder_dict[main_folder].append((formatted_date, date_obj, len(filenames)))

    # 폴더별 정보 출력
    for main_folder in sorted(folder_dict.keys()):
        # 실제 datetime 객체를 기반으로 정렬합니다.
        dates = sorted(folder_dict[main_folder], key=lambda x: x[1])
        
        subfolder_count = len(dates)
        percentage = subfolder_count / 208 * 100
        color = Fore.RESET

        print(f"{color}{main_folder}({percentage:.2f}%)")
        
        for date_str, _, count in dates:
            # 데이터 개수에 따른 색상 설정
            if count > 800:
                color = Fore.GREEN
            elif 500 <= count <= 800:
                color = Fore.BLUE
            elif 0 <= count <= 500:
                color = Fore.RED
            else:
                color = Fore.RESET

            print(f"{color}- {date_str}: {count}")
        
        print()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='computer (home/lab)')
    parser.add_argument('-c', '--com', type=str, required=False, default='lab', help='실행할 모드를 설정합니다.')
    args = parser.parse_args()

    if args.com in ['lab', 'l']:
        directory_path = "G:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/1_원본"
    elif args.com in ['home', 'h']:
        directory_path = "H:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/1_원본"
    else:
        print("wrong mode")

    count_files_in_directory(directory_path)
