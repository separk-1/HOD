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

def select_random_images(image_directory, n, exclude_images=None):
    image_paths = list_files_in_directory(image_directory)
    image_paths.sort()  # Sort images

    # Create candidate images list excluding images in exclude_images
    if exclude_images is not None:
        candidate_images = [image for image in image_paths if image not in exclude_images]
    else:
        candidate_images = image_paths

    # Determine the number of random images to select based on n
    num_images_to_select = min(n, len(candidate_images))

    # Select random images from candidate_images
    selected_images = random.sample(candidate_images, num_images_to_select)
    return selected_images

def copy_images_to_destination(image_list, destination_path):
    for image in image_list:
        destination_image_path = os.path.join(destination_path, os.path.basename(image))
        shutil.copy2(image, destination_image_path)
        print(f"Copied {image} to {destination_image_path}")

def copy_labels_to_destination(label_list, destination_path):
    for label in label_list:
        destination_label_path = os.path.join(destination_path, os.path.basename(label))
        shutil.copy2(label, destination_label_path)
        print(f"Copied {label} to {destination_label_path}")

def create_dataset(folders, drive_path, save_images_path, save_labels_path):
    # Check if the 'images' folder exists, if not, create it
    if not os.path.exists(save_images_path):
        os.makedirs(save_images_path)
    
    # Check if the 'labels' folder exists, if not, create it
    if not os.path.exists(save_labels_path):
        os.makedirs(save_labels_path)

    for folder in folders:
        cam_id = folder.split('_')[0]
        date = folder.split('_')[1]
        image_path = os.path.join(drive_path, 'images', cam_id, f"{cam_id}_{date}")
        label_path = os.path.join(drive_path, 'labels', cam_id, f"{cam_id}_{date}")
        labels = list_files_in_directory(label_path)
        n = len(labels)  # Set n to the number of labeled text files in the folder
        hanging_names = [label.replace("\\", '/').split('.')[0].split('/')[-1] for label in labels]

        # Create a set of excluded image paths
        hanging_images = set([os.path.join(image_path, name + ".png") for name in hanging_names])
        hanging_labels = set([os.path.join(label_path, name + ".txt") for name in hanging_names])

        nonhanging_images = select_random_images(image_path, n, hanging_images)

        print(f"Processing folder: {folder}")
        print(f"Selected random images from {image_path} and copying to {save_images_path}:")
        copy_images_to_destination(hanging_images, save_images_path)
        copy_images_to_destination(nonhanging_images, save_images_path)

        print(f"Copying labels to {save_labels_path}:")
        copy_labels_to_destination(hanging_labels, save_labels_path)
        create_empty_label_files(nonhanging_images, save_labels_path)


folders = ['D2_221201', 'D2_221202', 'D2_221203', 'D2_221205', 'D2_221206', 'D2_221207', 'D2_221208', 'D2_221209', 'D2_221210', 'D2_221212', 'D2_221213', 'D2_221214', 'D2_221215', 'D2_221216', 'D2_221217', 'D2_221219', 'D2_221220', 'D2_221221', 'D2_221222']

drive_path = 'D:/Dataset/Site_HD'
save_images_path = 'D:/Dataset/Sample/0919/images'
save_labels_path = 'D:/Dataset/Sample/0919/labels'

create_dataset(folders, drive_path, save_images_path, save_labels_path)
