import os
import xml.etree.ElementTree as ET
from glob import glob

def create_xml_annotation(filename, objects, img_size):
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "filename").text = filename
    
    for obj in objects:
        obj_element = ET.SubElement(annotation, "object")
        ET.SubElement(obj_element, "name").text = obj['name']
        bndbox = ET.SubElement(obj_element, "bndbox")
        ET.SubElement(bndbox, "xmin").text = str(obj['xmin'])
        ET.SubElement(bndbox, "ymin").text = str(obj['ymin'])
        ET.SubElement(bndbox, "xmax").text = str(obj['xmax'])
        ET.SubElement(bndbox, "ymax").text = str(obj['ymax'])
    
    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(img_size[0])
    ET.SubElement(size, "height").text = str(img_size[1])
    
    tree = ET.ElementTree(annotation)
    return tree

def convert_darknet_to_xml(label_path, img_size, class_names):
    objects = []
    with open(label_path, 'r') as file:
        for line in file.readlines():
            class_idx, x_center, y_center, width, height = map(float, line.split())
            try:
                name = class_names[int(class_idx)]
            except IndexError:
                print(f"Error in file {label_path}: "
                      f"class index {int(class_idx)} out of range. "
                      f"Available classes: {len(class_names)}")
                continue  # Skip this line and continue with the next one
            abs_width = width * img_size[0]
            abs_height = height * img_size[1]
            xmin = (x_center * img_size[0]) - (abs_width / 2)
            ymin = (y_center * img_size[1]) - (abs_height / 2)
            xmax = xmin + abs_width
            ymax = ymin + abs_height
            objects.append({
                'name': name,
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax
            })
    return objects

data_dir = "G:/내 드라이브/datasets/1008"
mode = 'test'
# Define your class names based on the Darknet .names file
class_names = ["hanging_object", "hanging_rope"]  # Replace with your actual class names

# Specify the paths to your Darknet label files and corresponding image size
label_paths = glob(f"{data_dir}/{mode}/labels/*.txt")  # Adjust path as needed
img_size = (1280, 720)  # Replace with your actual image size

# Convert each label file to XML
for label_path in label_paths:
    filename = os.path.basename(label_path).replace(".txt", "")
    objects = convert_darknet_to_xml(label_path, img_size, class_names)
    
    xml_tree = create_xml_annotation(filename, objects, img_size)
    xml_tree.write(f"{data_dir}/{mode}/labels_xml/{filename}.xml")  # Specify your desired output path
