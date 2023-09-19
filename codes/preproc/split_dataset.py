import os
import random
import shutil

def list_files_in_directory(directory):
    """
    List all files in the specified directory.

    Args:
        directory (str): Path to the directory.

    Returns:
        file_list (list): List of file names in the directory.
    """
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

def split_labels(labels_folder, train_folder, val_folder, split_ratio=0.9):
    # Create train and val folders if they do not exist
    if not os.path.exists(train_folder):
        os.makedirs(train_folder)
    if not os.path.exists(val_folder):
        os.makedirs(val_folder)

    # List all files in the labels folder
    label_files = os.listdir(labels_folder)

    # Calculate the number of labels for the train set
    num_train = int(len(label_files) * split_ratio)
    
    # Randomly shuffle the label files
    random.shuffle(label_files)

    # Split the label files into train and val sets
    train_labels = label_files[:num_train]
    val_labels = label_files[num_train:]

    # Move the train labels to the train folder
    for label in train_labels:
        src_path = os.path.join(labels_folder, label)
        dst_path = os.path.join(train_folder, label)
        shutil.move(src_path, dst_path)
        print(f"Moved {label} to {train_folder}")

    # Move the val labels to the val folder
    for label in val_labels:
        src_path = os.path.join(labels_folder, label)
        dst_path = os.path.join(val_folder, label)
        shutil.move(src_path, dst_path)
        print(f"Moved {label} to {val_folder}")

# 경로 설정
images_folder = 'D:/Dataset/Sample/0919/images'
train_images_folder = 'D:/Dataset/Sample/0919/train/images'
val_images_folder = 'D:/Dataset/Sample/0919/val/images'

labels_folder = 'D:/Dataset/Sample/0919/labels'
train_labels_folder = 'D:/Dataset/Sample/0919/train/labels'
val_labels_folder = 'D:/Dataset/Sample/0919/val/labels'

# 이미지 분할 (9:1 비율)
split_images(images_folder, train_images_folder, val_images_folder, split_ratio=0.9)

# 레이블 분할 (9:1 비율)
split_labels(labels_folder, train_labels_folder, val_labels_folder, split_ratio=0.9)
