import os
import xml.etree.ElementTree as ET
import cv2

# Darknet 형식의 레이블 파일 (객체 클래스, 중심 좌표, 너비, 높이)
darknet_labels_path = './sample.txt'

# Darknet 형식의 이미지 디렉토리
darknet_images_dir = './images/'

# Pascal VOC 형식으로 변환된 데이터를 저장할 디렉토리
output_dir = './'

# Pascal VOC 레이블 디렉토리 (이 디렉토리가 없으면 생성됩니다)
voc_labels_dir = os.path.join(output_dir, 'Annotations')
os.makedirs(voc_labels_dir, exist_ok=True)

# Pascal VOC 이미지 디렉토리 (이 디렉토리가 없으면 생성됩니다)
voc_images_dir = os.path.join(output_dir, 'JPEGImages')
os.makedirs(voc_images_dir, exist_ok=True)

# Darknet 레이블 파일을 읽어서 Pascal VOC 형식으로 변환
with open(darknet_labels_path, 'r') as darknet_labels_file:
    darknet_labels = darknet_labels_file.readlines()

for darknet_label in darknet_labels:
    parts = darknet_label.strip().split()
    image_path = os.path.join(darknet_images_dir, parts[0])
    image = cv2.imread(image_path)
    
    voc_label_path = os.path.join(voc_labels_dir, os.path.splitext(parts[0])[0] + '.xml')
    
    # Create an XML file in Pascal VOC format
    root = ET.Element('annotation')
    
    folder = ET.SubElement(root, 'folder')
    folder.text = 'JPEGImages'  # Pascal VOC 이미지 디렉토리 이름
    
    filename = ET.SubElement(root, 'filename')
    filename.text = os.path.splitext(parts[0])[0]  # 이미지 파일 이름
    
    size = ET.SubElement(root, 'size')
    width = ET.SubElement(size, 'width')
    height = ET.SubElement(size, 'height')
    depth = ET.SubElement(size, 'depth')
    
    width.text = str(image.shape[1])
    height.text = str(image.shape[0])
    depth.text = str(image.shape[2])
    
    # Darknet 형식의 레이블에서 클래스, 중심 좌표, 너비, 높이 추출
    class_id = parts[1]
    x_center = float(parts[2])
    y_center = float(parts[3])
    box_width = float(parts[4])
    box_height = float(parts[5])
    
    xmin = max(0, int((x_center - box_width / 2) * image.shape[1]))
    ymin = max(0, int((y_center - box_height / 2) * image.shape[0]))
    xmax = min(image.shape[1], int((x_center + box_width / 2) * image.shape[1]))
    ymax = min(image.shape[0], int((y_center + box_height / 2) * image.shape[0]))
    
    object_elem = ET.SubElement(root, 'object')
    name = ET.SubElement(object_elem, 'name')
    name.text = class_id
    
    bndbox = ET.SubElement(object_elem, 'bndbox')
    xmin_elem = ET.SubElement(bndbox, 'xmin')
    ymin_elem = ET.SubElement(bndbox, 'ymin')
    xmax_elem = ET.SubElement(bndbox, 'xmax')
    ymax_elem = ET.SubElement(bndbox, 'ymax')
    
    xmin_elem.text = str(xmin)
    ymin_elem.text = str(ymin)
    xmax_elem.text = str(xmax)
    ymax_elem.text = str(ymax)
    
    # Write the XML file
    tree = ET.ElementTree(root)
    tree.write(voc_label_path)

    # Copy the image to the Pascal VOC image directory
    voc_image_path = os.path.join(voc_images_dir, os.path.splitext(parts[0])[0] + '.jpg')
    cv2.imwrite(voc_image_path, image)
