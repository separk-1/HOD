# 해당 경로에 있는 모든 이미지에 대해 이름이 같고 비어 있는 txt 파일을 생성
import os

def list_files_in_directory(directory, allowed_extensions=[".png"]):
    """
    List all files with allowed extensions in the specified directory.

    Args:
        directory (str): Path to the directory.
        allowed_extensions (list): List of allowed file extensions.

    Returns:
        file_list (list): List of file names with allowed extensions in the directory.
    """
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in allowed_extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def create_empty_txt_files(directory, txt_save_path):
    image_files = list_files_in_directory(directory)
    for image_file in image_files:
        txt_filename = os.path.splitext(os.path.basename(image_file))[0] + ".txt"
        txt_filepath = os.path.join(txt_save_path, txt_filename)
        with open(txt_filepath, "w") as txt_file:
            pass
        print(f"Created empty txt file: {txt_filepath}")

# Specify the directory containing image files
image_directory = 'D:/Dataset/Sample/nh_images'

# Specify the directory to save txt files
txt_save_path = 'D:/Dataset/Sample/nh_labels'

create_empty_txt_files(image_directory, txt_save_path)
