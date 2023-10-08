import os
import random

def find_nonhanging(src_path, folder_list, exclude_list):
    matched_files = []
    
    for item_name in os.listdir(src_path):
        item_path = os.path.join(src_path, item_name)
        
        if os.path.isdir(item_path):
            for subitem_name in os.listdir(item_path):
                subitem_path = os.path.join(item_path, subitem_name)
                
                if os.path.isdir(subitem_path) and subitem_name in folder_list:
                    print(f"Exploring folder: {subitem_name}")
                    for filename in os.listdir(subitem_path):
                        file_path = os.path.join(subitem_path, filename)
                        if os.path.isfile(file_path):
                            # 파일 이름에서 확장자를 제거합니다.
                            name_without_extension, _ = os.path.splitext(filename)
                            # exclude_list에 없는 파일 이름만 추가합니다.
                            if name_without_extension not in exclude_list:
                                matched_files.append(name_without_extension)
    
    return matched_files

def save_to_txt(file_list, dest_path):
    sorted_files = sorted(file_list)
    
    with open(dest_path, 'w') as f:
        for filename in sorted_files:
            f.write(filename + "\n")

def load_txt(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f]

cam_list = ['D2', 'D3', 'D4', 'D8', 'S']
date_list = ['221201', '221202', '221203', '221205', '221206',
              '221207', '221208', '221209', '221210','221212',
              '221213', '221214', '221215', '221216', '221217'
              '221219', '221220', '221221', '221222', '221223']
mode = 'train'

folder_list = [f"{cam}_{date}" for cam in cam_list for date in date_list]

source_image_path = 'E:/Dataset/Site_HD/images'
label_path = f'G:/내 드라이브/datasets/1008/{mode}/hanging_list.txt'
target_txt_path = f'G:/내 드라이브/datasets/1008/{mode}/nonhanging_list.txt'
selected_txt_path = f'G:/내 드라이브/datasets/1008/{mode}/nonhanging_list_random.txt'

# target_txt_path에서 파일 이름을 로드합니다.
exclude_list = load_txt(label_path)

# exclude_list에 없는 파일 이름을 찾습니다.
matched_files = find_nonhanging(source_image_path, folder_list, exclude_list)

# target_txt_path의 라인 수와 동일한 개수의 파일 이름만 저장합니다.
save_to_txt(matched_files, target_txt_path)

all_nonhanging_files = load_txt(target_txt_path)

# all_nonhanging_files에서 len(exclude_list)만큼의 파일 이름을 무작위로 선택하여 저장합니다.
selected_files = random.sample(all_nonhanging_files, len(exclude_list))
save_to_txt(selected_files, selected_txt_path)