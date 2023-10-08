import shutil
import os

def copy_files_by_list(file_list_path, src_path, dest_path, extension):
    """
    file_list_path: 파일 이름이 저장된 텍스트 파일의 경로
    src_path: 원본 파일이 있는 경로
    dest_path: 파일을 복사하려는 경로
    """
    # 파일 리스트를 로드합니다.
    with open(file_list_path, 'r') as f:
        files_to_copy = [line.strip() for line in f]
    
    # 파일을 복사합니다.
    for filename in files_to_copy:
        cam_id = filename.split('_')[0]
        date = filename.split('_')[1]
        src_file_path = os.path.join(src_path, f'{cam_id}/{cam_id}_{date}/{filename}.{extension}')
        dest_file_path = os.path.join(dest_path, f'{filename}.{extension}')
        
        # 파일이 실제로 존재하는지 확인합니다.
        if os.path.exists(src_file_path):
            shutil.copy(src_file_path, dest_file_path)
            print(f"Copied: {filename}.{extension}")
        else:
            print(f"File not found: {src_file_path}")

def create_empty_label(file_list_path, src_path, dest_path, extension):
    with open(file_list_path, 'r') as f:
        files_to_copy = [line.strip() for line in f]
    
    for filename in files_to_copy:
        dest_file_path = os.path.join(dest_path, f'{filename}.{extension}')
        
        with open(dest_file_path, 'w') as f:
            pass
        print(f"Created empty file: {dest_file_path}.{extension}")

mode = 'train'

######hanging
file_list_path = f'G:/내 드라이브/datasets/1008/{mode}/hanging_list.txt'

## images
src_path = 'E:/Dataset/Site_HD/images'
dest_path = f'G:/내 드라이브/datasets/1008/{mode}/images'

copy_files_by_list(file_list_path, src_path, dest_path, 'png')

## labels
src_path = 'E:/Dataset/Site_HD/labels'
dest_path = f'G:/내 드라이브/datasets/1008/{mode}/labels'

copy_files_by_list(file_list_path, src_path, dest_path, 'txt')


######nonhanging
file_list_path = f'G:/내 드라이브/datasets/1008/{mode}/nonhanging_list_random.txt'

## images
src_path = 'E:/Dataset/Site_HD/images'
dest_path = f'G:/내 드라이브/datasets/1008/{mode}/images'

copy_files_by_list(file_list_path, src_path, dest_path, 'png')

## labels
src_path = 'E:/Dataset/Site_HD/labels'
dest_path = f'G:/내 드라이브/datasets/1008/{mode}/labels'

create_empty_label(file_list_path, src_path, dest_path, 'txt')