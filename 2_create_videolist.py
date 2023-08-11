import os
import re


##########SETTING###########
cam_list = [1, 2, 3, 4, 8]
############################
####### 0302까지 완료 #######

def replace_ip(match):
    ip_start = match.group(1)
    ip_end = match.group(3)
    return f'{ip_start}카메라{cam_id}_롯데 서초테라스힐_서초 테라스힐_{ip_end}'


for cam_id in cam_list:

    # 폴더 경로
    folder_path =  f'C:/Users/User/Downloads/D{cam_id}'
    output_file_path = f'./video_list/videolist_D{cam_id}.txt'
    file_names = os.listdir(folder_path)

    existing_names = set()
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as file:
            existing_names = set(line.strip() for line in file.readlines())

    # 텍스트 파일에 쓰기 (이어서 쓰기 모드 'a')
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for name in file_names:
            if name in existing_names:
                continue
            file.write(name.split('.')[0] + '\n')

    print(f'videolist_D{cam_id} 저장 완료')

    ######## 인코딩 오류 수정
    modified_lines = []
    with open(output_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            splits = line.split('_')
            video_id = splits[3]+'_'+splits[4]+'_'+splits[5]
            modified_line = f'IP 카메라{cam_id}_롯데 서초테라스힐_서초 테라스힐_{video_id}'
            modified_lines.append(modified_line)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(modified_lines)
    print('- 인코딩 수정 완료')

    ######## 중복된 줄 제거
    seen_lines = set()
    with open(output_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    unique_lines = [line for line in lines if not (line in seen_lines or seen_lines.add(line))]
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines)
    print('- 중복된 줄 제거 완료')

    ######## 정렬
    with open(output_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    sorted_lines = sorted(lines)
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.writelines(sorted_lines)
    print('- 줄 정렬 완료\n')
