import cv2
import os
import datetime
import argparse

##########SETTING###########
cam_list = [1, 2, 3, 4, 8]
interval = 30 #단위: sec
finish_list_path = './video_list/finishlist.txt'
skip_list_path = './video_list/skiplist.txt'
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
    start_time = video_id.split('_')[0]
    yy = start_time[2:4]
    mm = start_time[4:6]
    dd = start_time[6:8]
    hh = start_time[8:10]
    minmin = start_time[10:12]
    ss = int(start_time[12:14])
    
    elapsed_seconds = timestamp * 30  # 30초 단위로 변환
    new_ss = ss + elapsed_seconds
    
    new_hour_offset = new_ss // 3600
    new_minute_offset = (new_ss % 3600) // 60
    new_second_offset = new_ss % 60

    hh = str(int(hh) + new_hour_offset).zfill(2)
    minmin = str(int(minmin) + new_minute_offset).zfill(2)
    ss = str(new_second_offset).zfill(2)
    
    last_digit = timestamp % 2  # 0 또는 1
    
    corrected_time = correct_time_format(hh + minmin)
    return f'D{cam_id}_{yy}{mm}{dd}_{corrected_time}_{last_digit}.png'


parser = argparse.ArgumentParser(description='computer (home/lab)')
parser.add_argument('-c', '--com', type=str, required=False, default = 'lab', help='실행할 모드를 설정합니다.')
args = parser.parse_args()

# finishlist와 skiplist 읽기
finish_list = read_list_from_file(finish_list_path)
skip_list = read_list_from_file(skip_list_path)

finished_video_list = []
for cam_id in cam_list:
    count_finish = 0
    count_skip = 0

    file_path = f'./video_list/videolist_D{cam_id}_filtered.txt'

    video_list = read_list_from_file(file_path)

    for video_name in video_list:

        if video_name in finish_list:
            count_finish+=1
            #print(f'{video_name} 은(는) finishlist에 있으므로 스킵합니다.')
            continue

        if video_name in skip_list:
            count_skip += 1
            #print(f'{video_name} 은(는) skiplist에 있으므로 스킵합니다.')
            continue

        video_id = video_name.split('롯데 서초테라스힐_서초 테라스힐_')[1]
        video_date = video_id[2:8]

        # 동영상 파일 경로
        if args.com == 'lab' or args.com == 'l':
            video_path = f'C:/Users/SEPARK/Downloads/IP 카메라{cam_id}_롯데 서초테라스힐_서초 테라스힐_{video_id}.mp4'
        elif args.com == 'home' or args.com == 'h':
            video_path = f'C:/Users/User/Downloads/IP 카메라{cam_id}_롯데 서초테라스힐_서초 테라스힐_{video_id}.mp4'
        else:
            print("wrong com")

        # 파일이 존재하지 않으면 다음 비디오로 넘어감
        if not os.path.exists(video_path):
            #print(f'{video_path} 파일이 존재하지 않습니다. 건너뜁니다.')
            continue

        # 이미지를 저장할 폴더 생성
        date_folder = f'./output/D{cam_id}/D{cam_id}_{video_date}/'
        print(date_folder)
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)        
        
        # 동영상 파일 읽기
        video = cv2.VideoCapture(video_path)
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
                output_path = os.path.join(date_folder, generate_filename(cam_id, video_id, timestamp))
                cv2.imwrite(output_path, frame)
                print(f'{output_path} 저장 완료')
                timestamp += 1

            frame_count += 1

        video.release()
        print('이미지 추출 완료')
        
        finished_video_list.append(f'IP 카메라{cam_id}_롯데 서초테라스힐_서초 테라스힐_{video_id}')

    print(f'D{cam_id}: Completed {count_finish}, Remaining: {len(video_list)-count_finish}, Progress: {count_finish/len(video_list)*100:.2f}%')

print('기준: 221201~230302 (79일)')
print(f'이번에 처리한 비디오: {len(finished_video_list)}개')
for i in finished_video_list:
    print(i)

timenow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# 처리한 비디오들을 finishlist.txt에 추가
with open(finish_list_path, 'a', encoding='utf-8') as f:
    f.write('\n' + timenow + '\n')
    for video_id in finished_video_list:
        f.write(video_id + '\n')
    print(f'\n완료된 비디오 목록이 {finish_list_path}에 저장되었습니다.')
