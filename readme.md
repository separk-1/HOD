## 프로젝트 파이프라인

### 1. 시간대 필터링: `videolist_filtered`
- **시간대**: 오전 07시 ~ 오후 17시
- **제외**: 일요일

### 2. 파일 관리
- **이미 처리된 파일**: `finishlist`
- **스킵할 파일**: `skiplist`

### 3. 스크립트 작업 순서

1. **1_zip_to_imgs.py**
   - 서버에서 썸네일 이미지 다운로드
   - CCTV 폴더에 압축 해제

2. **2_create_videolist.py**
   - 썸네일 이미지로 영상 목록 추출
   - 중복제거/인코딩/정렬 기능 포함

3. **3_filter_videolist.py**
   - 주말 및 근무외 시간 제외 작업

4. **4_video_to_image.py**
   - 30초 간격으로 영상에서 이미지 추출
   - 이미지를 일별로 저장

### 4. 데이터 상태 확인: `status.py`
- 주요 폴더 및 하위 폴더의 데이터 파일 개수 확인
- 날짜 및 데이터 개수에 따른 색상 코드를 사용한 출력
- 각 메인 폴더 (예: D1, D2)의 하위 폴더의 퍼센티지를 출력