import zipfile
import os

##########SETTING###########
cam_list = [1, 2, 3, 4, 8]
############################
####### 0302까지 완료 #######

for cam_id in cam_list:

    # ZIP 파일이 있는 폴더 경로
    source_folder = 'C:/Users/User/Downloads/'

    # 압축을 해제할 폴더 경로
    destination_folder = os.path.join(source_folder, f'D{cam_id}')

    # 폴더 내의 파일 이름 가져오기
    zip_files = [name for name in os.listdir(source_folder) if name.endswith('.zip') and name.startswith(f'[D{cam_id}]')]

    # 해당 ZIP 파일들 압축 해제
    for zip_file in zip_files:
        zip_path = os.path.join(source_folder, zip_file)
        with zipfile.ZipFile(zip_path, 'r') as file:
            file.extractall(destination_folder)
        
        # ZIP 파일 삭제
        os.remove(zip_path)

    print(f'{len(zip_files)}개의 ZIP 파일을 {destination_folder} 폴더에 압축 해제하고 삭제 완료')
