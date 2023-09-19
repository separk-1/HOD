### video_to_image.py

특정 폴더에 있는 비디오 파일들에서 이미지 추출

#### 기능
1. finishlist와 skiplist 파일에서 비디오 이름을 읽음
2. 각 카메라별로 비디오 리스트를 읽어서 이미지를 추출
3. 추출한 이미지의 파일명을 생성하는 데 필요한 정보를 비디오 파일명에서 파싱

#### 주요 변수 설정
- `cam_list`: 처리할 카메라의 목록
- `interval`: 이미지를 추출할 간격 (초 단위)
- `finish_list_path` 및 `skip_list_path`: 처리 완료된 또는 스킵할 비디오의 목록이 저장된 파일 경로
- `save_path`: 비디오 파일이 복사될 로컬 경로

#### Sample Usage
```bash
python video_to_image.py -c [lab/home]
```

---

### status.py

- 지정된 디렉토리 내의 파일 수를 계산하여 콘솔에 출력하거나 텍스트 파일로 저장
- [여기](http://127.0.0.1:5000/)로 접속 시 웹페이지에서 확인 가능

#### 기능
1. 디렉토리 경로를 입력받음
2. 해당 경로에 있는 모든 파일 및 서브디렉토리를 탐색하여 파일 수 카운트

#### 주요 옵션
- `--com`: 디렉토리 경로를 지정 (lab, home, drive, backup 중 하나 선택)
- `--log`: 로그 저장 여부 설정. 이 옵션을 지정하면 결과가 status.txt 파일로 저장

#### Sample Usage
```bash
python status.py -c [lab/home/drive/backup] --log
```

---

### get_dataset.py

주어진 경로에서 데이터셋을 가져오는 스크립트

#### 기능
1. 이미지 및 레이블 데이터를 가져오기 위해 주어진 경로에서 파일 목록을 생성
2. 데이터셋 파일 목록을 생성하고 반환

#### 주요 변수 설정
- `dataset_path`: 데이터셋 파일을 가져올 경로

#### Sample Usage
```bash
python get_dataset.py
```

---

### split_dataset.py

데이터셋을 훈련 및 검증 세트로 분할하는 스크립트

#### 기능
1. 데이터셋을 훈련 및 검증 세트로 나누기 위해 데이터셋 파일 목록을 읽음
2. 주어진 비율에 따라 데이터셋을 나누고 훈련 및 검증 세트 파일 목록을 생성

#### 주요 변수 설정
- `dataset_path`: 데이터셋 파일을 가져올 경로
- `train_ratio`: 훈련 세트 비율 (0.0에서 1.0 사이의 값)
- `val_ratio`: 검증 세트 비율 (0.0에서 1.0 사이의 값)
- `output_path`: 분할된 데이터셋 파일 목록을 저장할 경로

#### Sample Usage
```bash
python split_dataset.py
```

---

### run_yolo.py

YOLO 모델을 실행하여 객체 검출 수행

#### 기능
1. YOLO 모델을 사용하여 주어진 이미지에서 객체 검출을 수행
2. 검출된 객체의 클래스 및 위치 정보를 반환

#### 주요 변수 설정
- `image_path`: 객체 검출을 수행할 이미지 파일의 경로
- `config_path`: YOLO 모델 구성 파일의 경로
- `weights_path`: 사전 훈련된 YOLO 모델 가중치 파일의 경로
- `class_path`: 객체 클래스 목록이 있는 파일의 경로

#### Sample Usage
```bash
python run_yolo.py -i [image_path] -c [config_path] -w [weights_path] -cl [class_path]
```
