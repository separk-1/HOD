import os
import random
import shutil
'''
def list_files_in_directory(directory):
    # List all files in the specified directory
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return sorted(file_list)

def create_empty_label_files(image_list, label_path):
    for image in image_list:
        image_name = os.path.basename(image)
        label_name = image_name.replace(".png", ".txt")
        label_file_path = os.path.join(label_path, label_name)
        with open(label_file_path, 'w') as empty_file:
            pass
        print(f"Created empty label file {label_file_path}")

def split_images(images_folder, train_folder, val_folder, split_ratio=0.9):
    # Create train and val folders if they do not exist
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    if not os.path.exists(val_folder):
        os.makedirs(val_folder)

    # List all files in the images folder
    image_files = os.listdir(images_folder)

    # Calculate the number of images for the train set
    num_train = int(len(image_files) * split_ratio)
    
    # Randomly shuffle the image files
    random.shuffle(image_files)

    # Split the image files into train and val sets
    train_images = image_files[:num_train]
    val_images = image_files[num_train:]

    # Move the train images to the train folder
    for image in train_images:
        src_path = os.path.join(images_folder, image)
        dst_path = os.path.join(train_folder, image)
        shutil.move(src_path, dst_path)
        print(f"Moved {image} to {train_folder}")

    # Move the val images to the val folder
    for image in val_images:
        src_path = os.path.join(images_folder, image)
        dst_path = os.path.join(val_folder, image)
        shutil.move(src_path, dst_path)
        print(f"Moved {image} to {val_folder}")
'''
# 경로 설정
images_folder = 'D:/Dataset/Sample/0919/images'
train_images_folder = 'D:/Dataset/Sample/0919/train/images'
val_images_folder = 'D:/Dataset/Sample/0919/val/images'

# 이미지 분할 (9:1 비율)
#split_images(images_folder, train_images_folder, val_images_folder, split_ratio=0.9)

labels_folder = 'D:/Dataset/Sample/0919/labels'
train_labels_folder = 'D:/Dataset/Sample/0919/train/labels'
val_labels_folder = 'D:/Dataset/Sample/0919/val/labels'

# train/images에 있는 이미지 파일 이름과 같은 labels 폴더 안의 txt 파일을 train/labels로 이동
for image_filename in os.listdir(train_images_folder):
    if image_filename.endswith('.png'):
        label_filename = image_filename.replace('.png', '.txt')
        src_label_path = os.path.join(labels_folder, label_filename)
        dst_label_path = os.path.join(train_labels_folder, label_filename)
        if os.path.exists(src_label_path):
            print(src_label_path, dst_label_path)
            shutil.move(src_label_path, dst_label_path)
            print(f"Moved {label_filename} to {train_labels_folder}")
