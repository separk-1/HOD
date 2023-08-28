import cv2
import os
import datetime
import argparse
import time
import shutil

##########SETTING###########
interval = 30 #단위: sec
finish_list_path = './video_list/finishlist.txt'
save_path = "C:/Users/SEPARK/Downloads" 
############################

def read_list_from_file(file_path):
    video_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    video_list = [line.strip() for line in lines]
    return video_list

def correct_time_format(time_str):
    hour = int(time_str[:2])
    minute = int(time_str[2:])

    # 60분을 넘어가면 시간을 1 증가시키고 분에서 60을 빼준다
    hour += minute // 60
    minute = minute % 60

    return f"{hour:02}{minute:02}"

def generate_filename(cam_id, video_id, timestamp):
    video_info = video_id.split('/')[1]  # "20230420_1319"
    date_str, time_str = video_info.split('_')  # "20230420", "1319"
    
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    hour = time_str[:2]
    minute = time_str[2:]
    
    elapsed_seconds = timestamp * 30  # 30초 단위로 변환
    new_minute_offset = elapsed_seconds // 60
    
    new_hour = int(hour) + new_minute_offset // 60
    new_minute = int(minute) + new_minute_offset % 60
    
    if new_minute >= 60:
        new_hour += 1
        new_minute -= 60
    
    last_digit = timestamp % 2  # 0 또는 1
    
    corrected_time = correct_time_format(f"{new_hour:02}{new_minute:02}")
    return f'{cam_id}_{year[2:]}{month}{day}_{corrected_time}_{last_digit}.png'


def get_single_avi_file(directory_path):
    try:
        avi_files = [file for file in os.listdir(directory_path) if file.endswith('.avi')]
        
        if len(avi_files) == 1:
            return avi_files[0]
        elif len(avi_files) == 0:
            return "해당 확장자를 가진 파일이 없습니다."
        else:
            return "여러 개의 확장자가 .avi인 파일이 있습니다."
    except Exception as e:
        return "오류 발생: " + str(e)
    
# 비디오 파일을 로컬로 복사합니다.
def copy_video_to_local(src, dst):
    shutil.copy(src, dst)

# finishlist와 skiplist 읽기
finish_list = read_list_from_file(finish_list_path)

timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
with open(finish_list_path, 'a', encoding='utf-8') as f:
    f.write('\n' + timenow + '\n')

finished_video_list = []
count_finish = 0
count_skip = 0

file_path = f'./video_list/videolist_S_filtered.txt'

video_list = read_list_from_file(file_path)

for video_id in video_list:

    if video_id in finish_list:
        count_finish+=1
        print(f'{video_id} 은(는) finishlist에 있으므로 스킵합니다.')
        continue

    video_date = video_id.split('/')[1][2:8]

    folder_path = f'//teamcovid.synology.me@SSL@6001/DavWWWRoot/CCTV/CCTV_Video/{video_id}/20{video_date}'
    video_name = get_single_avi_file(folder_path)
    video_path = f'{folder_path}/{video_name}'

    print(video_path)

    local_video_path = os.path.join(save_path, os.path.basename(video_path))

    # 파일이 네트워크 드라이브에 존재하면 로컬로 복사
    if os.path.exists(video_path):
        print(f'{video_path} 파일을 {local_video_path}로 복사합니다.')
        copy_video_to_local(video_path, local_video_path)
    else:
        print(f'{video_path} 파일이 존재하지 않습니다. 건너뜁니다.')
        continue

    # 이미지를 저장할 폴더 생성
    date_folder = f'D:/Dataset/Site/images/S/S_{video_date}/'
    print(video_path)
    if not os.path.exists(date_folder):
        os.makedirs(date_folder)        
    
    # 동영상 파일 읽기
    video = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    fps = int(video.get(cv2.CAP_PROP_FPS))

    # n초에 한 번 이미지를 추출하기 위한 간격 설정
    frame_interval = interval * fps
    
    # 이미지 추출
    frame_count = 0
    timestamp = 0
    while True:
        ret, frame = video.read()
        
        if not ret:
            break

        # n초 간격으로 이미지 저장
        if frame_count % frame_interval == 0:
            output_path = os.path.join(date_folder, generate_filename('S', video_id, timestamp))
            if not os.path.exists(output_path):  # 이미지가 존재하지 않을 경우만 저장
                # 화면에 표시
                success = cv2.imwrite(output_path, frame)
                if success:
                    print(f'{output_path} 저장 완료')
                else:
                    print(f'{output_path} 저장 실패')
            else:
                print(f'{output_path} 이미 존재하여 저장하지 않았습니다.')
            timestamp += 1

        frame_count += 1

    video.release()
    
    if frame_count > 0:
        completed_video = video_id
        finished_video_list.append(completed_video)

        # 처리한 비디오를 finishlist.txt에 추가
        with open(finish_list_path, 'a', encoding='utf-8') as f:
            f.write(completed_video + '\n')
        
        print(f'완료된 비디오 목록이 {finish_list_path}에 저장되었습니다.\n')

    # 로컬에 저장된 비디오 파일 제거
    if os.path.exists(local_video_path):
        os.remove(local_video_path)

print(f'이번에 처리한 비디오: {len(finished_video_list)}개')
for i in finished_video_list:
    print(i)

