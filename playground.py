from pascal import annotation_from_yolo
from pascal.utils import save_xml
import os

def list_text_files(folder_path):
    """
    List all text files in the given folder.
    Args:
    - folder_path (str): Path to the folder to search
    Returns:
    - List of text file names (List[str])
    """
    text_files = []
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and entry.name.endswith('.txt'):
                text_files.append(entry.name)
    return text_files

def main():
    # Define the label map
    label_map = {
        0: "hanging_object",
        1: "hanging_rope"
    }

    # Define the modes to process
    modes = ['train']

    # Loop through each mode and process files
    for mode in modes:
        label_path = f'../Colab/Dataset/0919/{mode}/labels'
        text_files = list_text_files(label_path)

        for file in text_files:
            filename = file.split('.')[0]
            
            # Convert YOLO annotations to PASCAL VOC format
            ann = annotation_from_yolo(
                f"{label_path}/{filename}.txt",
                label_map=label_map,
                img_w=1280,
                img_h=720)
            
            # Convert annotation to XML and save
            xml = ann.to_xml()
            save_xml(f"../Colab/Dataset/0919/{mode}/labels_xml/{filename}.xml", xml)

if __name__ == "__main__":
    main()
