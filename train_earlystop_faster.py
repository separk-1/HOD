import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.datasets import CocoDetection
from torchvision import transforms
from tqdm import tqdm

## 코드 수정 필요
# 사용자 정의 데이터 묶음 함수(collate function)
def collate_fn(batch):
    return tuple(zip(*batch))

def validate(model, val_data_loader, device):
    model.eval()
    total_loss = 0.0

    with torch.no_grad():
        for images, targets in val_data_loader:
            images = list(image.to(device) for image in images)
            
            processed_targets = []
            for t in targets:
                if isinstance(t, dict):
                    processed_targets.append({k: v.to(device) for k, v in t.items()})
                else:
                    processed_targets.append({
                        'boxes': torch.zeros((0, 4), dtype=torch.float32, device=device),
                        'labels': torch.zeros(0, dtype=torch.int64, device=device),
                    })

            # Set model to training mode temporarily to get loss_dict
            model.train()
            loss_dict = model(images, processed_targets)

            model.eval()  # Set it back to evaluation mode

            losses = sum(loss for loss in loss_dict.values())
            total_loss += losses.item()

    average_loss = total_loss / len(val_data_loader)
    return average_loss




def main():
    num_epochs = 100  # 전체 데이터셋을 학습할 횟수
    batch_size = 4 # 한 번에 n개의 샘플을 가져옴

    # Check if CUDA is available and print
    if torch.cuda.is_available():
        print("CUDA is available. Using GPU.")
    else:
        print("CUDA is not available. Using CPU.")
        exit()
    
    # COCO 데이터셋을 불러옴. 이미지는 Tensor로 변환됨.
    train_dataset = CocoDetection(root='./datasets/D1/images/',
                                annFile='./datasets/D1/D1_COCO.json',
                                transform=transforms.ToTensor())

    # DataLoader를 사용해 데이터를 묶음
    train_data_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,  
        shuffle=True,  # 데이터를 섞음
        num_workers=4,  # 데이터 로딩을 위해 4개의 작업자(sub-process)를 사용
        collate_fn=collate_fn  # 사용자 정의 데이터 묶음 함수 사용
    )

    # 미리 훈련된 Faster R-CNN 모델을 불러옴
    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True) #일단 transfer learning으로 했는데, 우리 목적을 위해서는 from scrach가 좋을 것 같음. 데이터셋 쌓이면 변경

    # 분류기를 새로운 것으로 교체. 여기서는 두 개의 클래스가 있다고 가정 (배경 포함).
    num_classes = 2
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    # GPU가 사용 가능하면 GPU를 사용, 아니면 CPU를 사용
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    # 학습 가능한 모델 파라미터를 가져옴
    params = [p for p in model.parameters() if p.requires_grad]

    # SGD 옵티마이저 설정
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)

    # 모델을 디바이스에 할당
    model.to(device)

    # 모델을 학습 모드로 설정
    model.train()

    val_dataset = CocoDetection(root='./datasets/D1/images/',
                                annFile='./datasets/D1/D1_COCO.json',
                                transform=transforms.ToTensor())

    val_data_loader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=4,
        collate_fn=collate_fn
    )

    best_loss = float('inf')
    patience = 5  # 연속적으로 향상되지 않은 에폭 수
    early_stop_counter = 0

    print("Training started...")
    for epoch in range(num_epochs):
        print(f"Starting epoch {epoch + 1}")

        pbar = tqdm(train_data_loader, desc=f"Epoch {epoch + 1}")
        for images, targets in pbar:
            images = list(image.to(device) for image in images)
            
            processed_targets = []
            for t in targets:
                if isinstance(t, dict):
                    processed_targets.append({k: v.to(device) for k, v in t.items()})
                else:
                    processed_targets.append({
                        'boxes': torch.zeros((0, 4), dtype=torch.float32, device=device),
                        'labels': torch.zeros(0, dtype=torch.int64, device=device),
                    })

            loss_dict = model(images, processed_targets)
            losses = sum(loss for loss in loss_dict.values())
            
            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            pbar.set_postfix({"Batch Loss": losses.item()})
    
        # Validate the model
        val_loss = validate(model, val_data_loader, device)
        print(f"Validation loss: {val_loss}")

        # Check for early stopping
        if val_loss < best_loss:
            best_loss = val_loss
            early_stop_counter = 0
            torch.save(model.state_dict(), f'fasterrcnn_resnet50_fpn_best.pth')
        else:
            early_stop_counter += 1
            if early_stop_counter >= patience:
                print(f"Validation loss hasn't improved for {patience} epochs. Early stopping...")
                break

    print("Training completed.")

    torch.save(model.state_dict(), f'fasterrcnn_resnet50_fpn_{num_epochs}.pth')

if __name__ == '__main__':
    main()
