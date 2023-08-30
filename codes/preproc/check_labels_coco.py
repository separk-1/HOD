import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

# Path to COCO annotation file
coco_annotation_file = "../../datasets/sample/coco_annotations.json"

# Load COCO annotations
with open(coco_annotation_file, "r") as f:
    coco_annotations = json.load(f)

# Load an image for visualization
image_id = 129  # Change this to the desired image ID
image_filename = coco_annotations["images"][image_id]["file_name"]
image_path = os.path.join("./datasets/sample/images", image_filename)
image = Image.open(image_path)

# Get annotations for the selected image
annotations = [anno for anno in coco_annotations["annotations"] if anno["image_id"] == image_id]

# Create a subplot for image and annotations
fig, ax = plt.subplots(1)
ax.imshow(image)

# Draw bounding boxes on the image
for annotation in annotations:
    bbox = annotation["bbox"]
    rect = Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=2, edgecolor="r", facecolor="none")
    ax.add_patch(rect)

# Show the image with bounding boxes
plt.axis("off")
plt.show()
