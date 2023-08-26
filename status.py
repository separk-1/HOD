import os
from datetime import datetime
from colorama import Fore
import argparse

def extract_date(date_string):
    """날짜 형식 변환: 230109 -> 23년 1/9(요일)"""
    month = int(date_string[-4:-2])
    day = int(date_string[-2:])
    year = 2000 + int(date_string[:-4])
    date_obj = datetime(year, month, day)
    weekdays_kr = ["월", "화", "수", "목", "금", "토", "일"]
    return f"{year-2000}년 {month}/{day}({weekdays_kr[date_obj.weekday()]})", date_obj

def count_files_in_directory(path, output_file=None):
    if not os.path.exists(path):
        print("지정된 경로가 존재하지 않습니다.")
        return
    if not os.path.isdir(path):
        print("지정된 경로는 디렉토리가 아닙니다.")
        return

     # Directory path 정보를 txt 파일 맨 앞에 추가
    if output_file:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        output_file.write(f"Timestamp: {current_time}\n")
        output_file.write(f"Directory Path: {path}\n\n")

    folder_dict = {}
    for foldername, _, filenames in os.walk(path):
        parts = foldername.split(os.path.sep)
        if len(parts) < 3:
            continue

        main_folder = parts[-2]
        date_folder = parts[-1].split('_')[-1]

        if date_folder.isdigit():
            formatted_date, date_obj = extract_date(date_folder)
            folder_dict.setdefault(main_folder, []).append((formatted_date, date_obj, len(filenames)))

    for main_folder in sorted(folder_dict):
        dates = sorted(folder_dict[main_folder], key=lambda x: x[1])
        subfolder_count = len(dates)
        percentage = subfolder_count / 208 * 100
        
        message = f"{main_folder}({percentage:.2f}%)"
        print(message)
        if output_file:
            output_file.write(message + '\n')

        for date_str, date, count in dates:
            # 데이터 개수에 따른 색상 설정
            if count > 800:
                color = Fore.GREEN
            elif 500 <= count <= 800:
                color = Fore.BLUE
            elif 0 <= count <= 500:
                color = Fore.RED
            else:
                color = Fore.RESET    

            completion_str = ''
            # D{cam_id}_date 폴더 존재 여부 확인
            parent_dir = f"D:/LOTTE/labels/{main_folder}/"
            target_prefix = f"{main_folder}_{date.strftime('%y%m%d')}"

            if any(item.startswith(target_prefix) for item in os.listdir(parent_dir)):
                completion_str = " (labeled)"

            message = f"{color}- {date_str}: {count}{completion_str}{Fore.RESET}"
            print(message)
            if output_file:
                output_file.write(f"- {date_str}: {count}{completion_str}\n")
        
        
        print()
        if output_file:
            output_file.write('\n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Specify computer type')
    parser.add_argument('-c', '--com', choices=['lab', 'l', 'home', 'h', 'drive', 'd', 'backup', 'b'], default='backup', help='실행할 모드를 설정합니다.')
    parser.add_argument('-l', '--log', action='store_true', default = True, help='log 저장 여부를 설정합니다.')
    args = parser.parse_args()

    paths = {
        'lab': "G:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/output",
        'l': "G:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/output",
        'home': "H:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/output",
        'h': "H:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/output",
        'drive': "E:/images",
        'd': "E:/images",
        'backup': "D:/LOTTE/images",
        'b': "D:/LOTTE/images"
    }
    
    directory_path = paths.get(args.com, None)
    if not directory_path:
        print("wrong mode")
        exit()

    if args.log == True:
        with open('G:/내 드라이브/0. Run/1. Research/2. HangingObjectDetection/HOD/app/status.txt', 'w', encoding='utf-8') as f:
            count_files_in_directory(directory_path, f)
    else:
        count_files_in_directory(directory_path)

