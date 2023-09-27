import torch
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.datasets import CocoDetection
from torchvision import transforms
from tqdm import tqdm
from datetime import datetime

# 사용자 정의 데이터 묶음 함수(collate function)
def collate_fn(batch):
    return tuple(zip(*batch))

def main():
    now = datetime.now()
    timestamp = now.strftime("%y%m%d_%H%M%S")

    num_epochs = 10
    batch_size = 4  # Reduced batch size

    if torch.cuda.is_available():
        print("CUDA is available. Using GPU.")
    else:
        print("CUDA is not available. Using CPU.")
        exit()

    train_dataset = CocoDetection(root='../Colab/Dataset/0919/train/images/',
                                  annFile='../Colab/Dataset/0919/coco_train.json',
                                  transform=transforms.ToTensor())

    train_data_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=2,  # Reduced num_workers
        collate_fn=collate_fn
    )

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    
    num_classes = 2
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.005, momentum=0.9, weight_decay=0.0005)

    model.to(device)
    model.train()

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

        # Clear GPU cache
        torch.cuda.empty_cache()

    print("Training completed.")
    torch.save(model.state_dict(), f'./results/{timestamp}_{epoch}.pth')

if __name__ == '__main__':
    main()
