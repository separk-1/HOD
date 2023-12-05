# HangCon: A New Benchmark Dataset for Hanging Object Detection in Construction Sites
## `video_to_image.py` - Image Extraction from Videos

Transforms videos into a series of images, extracting frames from video files located within a specified directory.

### Features
- Reads video names from `finishlist` and `skiplist`.
- Processes video lists by camera type to extract images.
- Parses necessary information from video filenames to create image filenames.

### Configuration Variables
- `cam_list`: List of cameras to be processed.
- `interval`: Interval for image extraction (in seconds).
- `finish_list_path`, `skip_list_path`: Paths to files containing lists of videos that have been processed or are to be skipped.
- `save_path`: Local path where extracted video files will be saved.

### Sample Usage
```bash
python video_to_image.py -c [lab/home]
```

---

## `status.py` - Directory File Count

Counts files within a specified directory, providing output in the console or saving it to a text file, also accessible via a web page [here](http://127.0.0.1:5000/).

### Features
- Accepts a directory path as input.
- Counts all files and subdirectories within the given path.

### Key Options
- `--com`: Specify the directory path (choose from lab, home, drive, backup).
- `--log`: Toggle log saving. If specified, results are saved to `status.txt`.

### Sample Usage
```bash
python status.py --com [lab/home/drive/backup] --log
```

---

## `get_dataset.py` - Retrieve Dataset

A script to gather image and label data from a given path, creating and returning a dataset file list.

### Features
- Generates a file list from the given path to retrieve images and label data.
- Creates and returns a dataset file list.

### Configuration Variables
- `dataset_path`: Path from where dataset files will be retrieved.

### Sample Usage
```bash
python get_dataset.py
```

---

## `split_dataset.py` - Dataset Division

Splits datasets into training and validation sets, organizing data for efficient model training.

### Features
- Reads the dataset file list to divide into training and validation sets.
- Splits the dataset according to the given ratio, creating file lists for both sets.

### Configuration Variables
- `dataset_path`: Path from where dataset files will be retrieved.
- `train_ratio`: Ratio of the dataset to be used for training (value between 0.0 and 1.0).
- `val_ratio`: Ratio of the dataset to be used for validation (value between 0.0 and 1.0).
- `output_path`: Path where the split dataset file lists will be saved.

### Sample Usage
```bash
python split_dataset.py
```

---

## `run_yolo.py` - Object Detection with YOLO

Executes YOLO model for object detection in images, returning class and position information of detected objects.

### Features
- Utilizes YOLO model for detecting objects in provided images.
- Returns the class and location information of detected objects.

### Configuration Variables
- `image_path`: Path of the image file on which object detection will be performed.
- `config_path`: Path of the YOLO model configuration file.
- `weights_path`: Path of the pre-trained YOLO model weights file.
- `class_path`: Path of the file containing a list of object classes.

### Sample Usage
```bash
python run_yolo.py -i [image_path] -c [config_path] -w [weights_path] -cl [class_path]
```
