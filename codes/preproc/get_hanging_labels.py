import os
import shutil
#이미지에 맞게 label 얻어오기

def main(source_path, target_path):
    source_labels_path = f'{source_path}/labels' #원본 라벨 경로
    target_image_path = f'{target_path}/images' #타겟 이미지 경로
    target_label_path = f'{target_path}/labels'
    
    image_files = [f for f in os.listdir(target_image_path) if f.endswith('.png')] #타겟 이미지 파일 목록
    
    for image_file in image_files:
        image_name = os.path.splitext(image_file)[0]
        cam_id = image_name.split('_')[0]
        date = image_name.split('_')[1]
        date_folder = f'{cam_id}_{date}'
        txt_file_path = f'{source_labels_path}/{cam_id}/{date_folder}/{image_name}.txt'
        
        if os.path.exists(txt_file_path): #원본 경로에 이미지 이름과 동일한 라벨파일 존재하면
            target_txt_path = f'{target_label_path}/{image_name}.txt' #타겟 경로에 복사
            shutil.copy(txt_file_path, target_txt_path)
            print(txt_file_path, target_txt_path)
        else:
            print(f"No corresponding txt file found for {image_file}")

if __name__ == "__main__":
    source_path = "D:/Dataset/Site_downsized"  # 원본 위치
    target_path = "D:/Dataset/Sample"  # 저장할 위치
    main(source_path, target_path)