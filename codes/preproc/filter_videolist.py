import datetime

##########SETTING###########
cam_list = [1, 2, 3, 4, 8]
############################


def filter_video_time(video_name):
    # 영상의 시작 및 종료 시간을 추출
    start_time_str, end_time_str = video_name.split('_')[3:5]
    if '235959' in start_time_str:
        print(f"제외된 영상(235959): {video_name}")
        return False
    
    # 추출된 시간 문자열을 datetime 객체로 변환
    start_time = datetime.datetime.strptime(start_time_str, '%Y%m%d%H%M%S')
    end_time = datetime.datetime.strptime(end_time_str, '%Y%m%d%H%M%S')
    
    # 주어진 조건에 따라서 영상을 필터링
    if start_time.weekday() == 6 or end_time.weekday() == 6:  # 일요일 체크
        print(f"제외된 영상(일요일): {video_name}")
        return False
    if start_time.date() != end_time.date() and (start_time.weekday() == 6 or (end_time - datetime.timedelta(days=1)).weekday() == 6):
        print(f"제외된 영상(시작-종료 사이 일요일): {video_name}")
        return False  # 시작과 종료의 날짜가 다르고, 그 사이에 일요일이 있는 경우 체크
    if start_time.time() < datetime.time(7, 0) or end_time.time() > datetime.time(17, 0):  # 근무시간: 07~17. 
        print(f"제외된 영상(시간대 초과): {video_name}")
        return False
    return True

for cam_num in cam_list:
    filtered_videos = []
    with open(f'../../config/videolist_D{cam_num}.txt', "r", encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            if filter_video_time(line):
                filtered_videos.append(line)
    # 필터링된 결과를 파일에 저장
    with open(f'../../config/videolist_D{cam_num}_filtered.txt', "w", encoding='utf-8') as f:
        for video in filtered_videos:
            f.write(video + '\n')

    print(f"필터링된 영상 목록이 videolist_D{cam_num}_filtered.txt 파일에 저장되었습니다.")