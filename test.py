import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from torchvision import transforms
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.ops import box_iou
from tqdm import tqdm
import torch
from torchvision.datasets import CocoDetection
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from datetime import datetime

def evaluate_model(model, test_data_loader, timestamp):
    model.eval()
    count = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, targets in tqdm(test_data_loader, desc="Testing"):
            images = [img.to(device) for img in images]
            predictions = model(images)

            for prediction, target in zip(predictions, targets):
                pred_labels = prediction['labels'].cpu().numpy()

                true_labels = None
                if target:  # Check if target list is not empty
                    true_labels = target[0].get('category_id', None)  # Assuming the first dictionary has the category_id

                if true_labels is not None:
                    all_labels.append(true_labels)
                else:
                    all_labels.append(-1)  # Placeholder for missing label

                if len(pred_labels) > 0:
                    all_preds.extend(pred_labels)
                else:
                    all_preds.append(-1)  # Placeholder for missing prediction

                if count < 100:
                    count += 1
                    fig, ax = plt.subplots(1)
                    
                    # Add actual image first
                    ax.imshow(images[0].cpu().permute(1, 2, 0))
                    
                    # Turn off the axis
                    ax.axis('off')
                    
                    for box in prediction['boxes'].cpu().detach().numpy():
                        x, y, xmax, ymax = box
                        rect = Rectangle((x, y), xmax-x, ymax-y, linewidth=1, edgecolor='r', facecolor='none')
                        ax.add_patch(rect)

                    if target:  # Check if target list is not empty
                        x, y, xmax, ymax = target[0]['bbox']  # Assuming the first dictionary has the bbox
                        rect = Rectangle((x, y), xmax-x, ymax-y, linewidth=1, edgecolor='g', facecolor='none')
                        ax.add_patch(rect)
                        
                    plt.savefig(f"results/{timestamp}_test_{count}.png")



    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    f1 = f1_score(all_labels, all_preds, average='weighted')
    accuracy = accuracy_score(all_labels, all_preds)

    print(f'Precision: {round(precision, 3)}')
    print(f'Recall: {round(recall, 3)}')
    print(f'F1 Score: {round(f1, 3)}')
    print(f'Accuracy: {round(accuracy, 3)}')


if __name__ == '__main__':
    current_time = datetime.now()
    timestamp = current_time.strftime("%y%m%d_%H%M")
    print(timestamp)

    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

    model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
    num_classes = 2
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model.load_state_dict(torch.load('./results/fasterrcnn_resnet50_fpn_D1_49.pth'))
    model.to(device)
    model.eval()

    test_dataset = CocoDetection(root='./datasets/D1/images/',
                                 annFile='./datasets/D1/D1_COCO.json',
                                 transform=transforms.ToTensor())

    test_data_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=1,
        shuffle=False,
        num_workers=0,  # 4로 하면 더 빨라짐
        collate_fn=lambda x: tuple(zip(*x))
    )

    print("Starting testing...")

    evaluate_model(model, test_data_loader, timestamp)
