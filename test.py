from torchvision.ops import box_iou
from tqdm import tqdm
import torch
from torchvision.datasets import CocoDetection

# 모델을 불러옵니다
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
num_classes = 2  # 포함된 클래스 수 (배경 포함)
in_features = model.roi_heads.box_predictor.cls_score.in_features
model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
model.load_state_dict(torch.load('fasterrcnn_resnet50_fpn.pth'))
model.to(device)

# 사용자 정의 데이터 묶음 함수(collate function)
def collate_fn(batch):
    return tuple(zip(*batch))

def evaluate_model(model, test_data_loader):
    model.eval()
    
    # Precision, Recall, AP를 저장하기 위한 변수
    total_true_positives = 0
    total_false_positives = 0
    total_false_negatives = 0
    
    with torch.no_grad():
        for images, targets in tqdm(test_data_loader, desc="Testing"):
            images = [img.to(device) for img in images]
            
            # 모델 예측
            predictions = model(images)
            
            for prediction, target in zip(predictions, targets):
                # 이 부분에서 각 이미지에 대한 성능 지표를 계산하고 누적
                iou = box_iou(target['boxes'].to(device), prediction['boxes'])
                
                # 여기서는 간단하게 IoU가 0.5 이상인 경우를 True Positive로 취급합니다.
                # IoU 임계값, NMS 등에 따라 실제 구현은 달라질 수 있습니다.
                true_positives = (iou > 0.5).sum().item()
                false_positives = prediction['boxes'].shape[0] - true_positives
                false_negatives = target['boxes'].shape[0] - true_positives
                
                total_true_positives += true_positives
                total_false_positives += false_positives
                total_false_negatives += false_negatives
                
    precision = total_true_positives / (total_true_positives + total_false_positives)
    recall = total_true_positives / (total_true_positives + total_false_negatives)
    
    # Precision과 Recall을 이용해 F1 Score와 AP를 계산할 수 있습니다.
    f1_score = 2 * (precision * recall) / (precision + recall)
    
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1_score}")

# main 함수에서 evaluate_model 함수 호출
if __name__ == '__main__':
    # 테스트 데이터셋 로드 (여기서는 학습 데이터셋과 같은 데이터셋을 사용했지만, 실제로는 다른 데이터셋을 사용해야 함)
    test_dataset = CocoDetection(root='./datasets/sample/images/',
                                annFile='./datasets/sample/coco_annotations.json',
                                transform=transforms.ToTensor())

    test_data_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=4,
        collate_fn=collate_fn
    )

    print("Starting testing...")

    # 테스트 루프
    with torch.no_grad():
        for images, targets in tqdm(test_data_loader):
            images = list(image.to(device) for image in images)

            # 예측
            prediction = model(images)
            
            # 여기서 prediction을 이용하여 성능을 평가할 수 있습니다.

    evaluate_model(model, test_data_loader)

