import shutil
import os

def copy_files(src_path, dest_path, folder_list):
    """
    src_path: 원본 파일이 있는 경로
    dest_path: 파일을 복사하려는 경로
    folder_list: 복사하려는 파일이 포함된 폴더의 이름 목록
    """
    for folder_name in folder_list :
        folder_path = os.path.join(src_path, folder_name)
        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    shutil.copy(file_path, dest_path)
        else:
            print(f"{folder_name} does not exist in {src_path}")

source_path = 'E:/Dataset/Site_HD/images'
target_path = 'G:/내 드라이브/datasets/1008/test/images'
cam_list = ['D2', 'D3', 'D4', 'D8', 'S']
date_list = ['230224', '230225', '230227', '230228', '230301', '230302']
copy_files(source_path, target_path, test_list)