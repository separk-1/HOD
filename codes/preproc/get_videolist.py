# 경로 내의 동영상 파일 목록 저장

import os

disk_path = 'E:/서초테라스힐'
dates = os.listdir(disk_path)
cam_ids = [2, 3, 4, 8]

# 파일 확장자 리스트
video_extensions = ['.mp4']

for cam_id in cam_ids:
    for date in dates:
        output_file_path = f'../../config/videolist_D{cam_id}.txt'
        directory_path = f'{disk_path}/{date}/[D{cam_id}]IPdome'
        
        with open(output_file_path, 'a', encoding= 'utf-8') as output_file:
            file_names = os.listdir(directory_path)
            for file_name in file_names:
                absolute_file_path = os.path.join(directory_path, file_name)
                
                if os.path.isfile(absolute_file_path) and os.path.splitext(file_name)[1].lower() in video_extensions:
                    output_file.write(file_name.split('.')[0] + '\n')
        print(f'D{cam_id} {date}')
