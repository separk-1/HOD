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

지정된 디렉토리 내의 파일 수를 계산하여 콘솔에 출력하거나 텍스트 파일로 저장
[여기](http://127.0.0.1:5000/)로 접속 시 웹페이지에서 확인 가능

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