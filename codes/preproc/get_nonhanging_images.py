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

def select_random_images(image_directory, last_filename, n=5, exclude_images=None):
    image_paths = list_files_in_directory(image_directory)
    image_paths.sort()  # Sort images
    
    # Find the index of the last_filename
    last_index = image_paths.index(os.path.join(image_directory, last_filename + ".png"))

    # Create candidate images list excluding images in exclude_images
    candidate_images = [image for image in image_paths if image not in exclude_images]

    # Select random images within the range up to last_index
    selected_indices = random.sample(range(last_index + 1), min(n, last_index + 1))
    selected_images = [candidate_images[i] for i in selected_indices]
    return selected_images


folders = ['D1_221201', 'D1_230102', 'D1_230103', 'D2_221201', 'D2_230102', 'D3_221201', 'D3_230103', 'S_221201', 'S_230102']

drive_path = 'D:/Dataset/Site_downsized'
save_path = 'D:/Dataset/Sample/nh_images'
n = 10

for folder in folders:
    cam_id = folder.split('_')[0]
    date = folder.split('_')[1]
    image_path = f'{drive_path}/images/{cam_id}/{cam_id}_{date}'
    label_path = f'{drive_path}/labels/{cam_id}/{cam_id}_{date}'
    labels = list_files_in_directory(label_path)
    label_names = [label.replace("\\", '/').split('.')[0].split('/')[-1] for label in labels]
    
    last_filename = label_names[-1]
    
    # Create a set of excluded image paths
    exclude_images = set([os.path.join(image_path, name + ".png") for name in label_names])

    selected_images = select_random_images(image_path, last_filename, n, exclude_images)
    print(f"Selected random images from {image_path}:")
    for image in selected_images:
        destination_image_path = os.path.join(save_path, os.path.basename(image))
        shutil.copy2(image, destination_image_path)
        print(f"Copied {image} to {destination_image_path}")
