from PIL import Image
import os

def copy_and_resize_images(source_dir, destination_dir, target_size=(1280, 720), allowed_extensions=[".png"]):
    """
    Copy image files from source directory to destination directory while maintaining folder structure and resizing.

    Args:
        source_dir (str): Source directory containing image files.
        destination_dir (str): Destination directory to copy image files to.
        target_size (tuple): Target size for resizing (width, height).
        allowed_extensions (list): List of allowed image file extensions.
    """
    error_count = 0
    for root, _, files in os.walk(source_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in allowed_extensions):
                source_path = os.path.join(root, file)
                relative_path = os.path.relpath(source_path, source_dir)
                destination_path = os.path.join(destination_dir, relative_path)

                if os.path.exists(destination_path):
                    print(f"Image already exists in destination: {destination_path}")
                    continue  # Skip copying if image already exists

                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                try:
                    # Resize the image while copying
                    with Image.open(source_path) as img:
                        resized_img = img.resize(target_size, Image.ANTIALIAS)
                        resized_img.save(destination_path, format='png')  # You can adjust the format if needed

                    print(f"Copied and resized: {source_path} to {destination_path}")
                except OSError as e:
                    print(f"Error occurred while processing image: {e}")
                    error_count+=1
                    continue  # Skip to the next image in case of an error
    return error_count


# Example usage
source_directory = "D:/Dataset/Site/images/D1"
destination_directory = "E:/images"

error_count = copy_and_resize_images(source_directory, destination_directory)
print(f'error image count: {error_count}')