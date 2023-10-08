import os
'''
경로의 hanging 파일 목록을 txt로 저장
'''
def find_hanging(src_path, folder_list):
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
                            matched_files.append(name_without_extension)
    
    return matched_files

def save_to_txt(file_list, dest_path):
    # 파일 이름을 알파벳 순서대로 정렬합니다.
    sorted_files = sorted(file_list)
    
    with open(dest_path, 'w') as f:
        for filename in sorted_files:
            f.write(filename + "\n")

cam_list = ['D2', 'D3', 'D4', 'D8', 'S']
date_list = ['221201', '221202', '221203', '221205', '221206',
              '221207', '221208', '221209', '221210','221212',
              '221213', '221214', '221215', '221216', '221217'
              '221219', '221220', '221221', '221222', '221223']
mode = 'train'

folder_list = [f"{cam}_{date}" for cam in cam_list for date in date_list]

source_label_path = 'E:/Dataset/Site_HD/labels'
target_txt_path = f'G:/내 드라이브/datasets/1008/{mode}/hanging_list.txt'

matched_files = find_hanging(source_label_path, folder_list)
save_to_txt(matched_files, target_txt_path)
