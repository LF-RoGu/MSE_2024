import torch
import torch.nn as nn
from torchvision import datasets, models, transforms
from torch.utils.data import DataLoader
import os

def evaluate_model(model, dataloaders, dataset_sizes, device):
    model.eval()   # Set model to evaluate mode
    running_corrects = 0

    # Iterate over validation data
    for inputs, labels in dataloaders['val']:
        inputs = inputs.to(device)
        labels = labels.to(device)

        # Forward
        with torch.set_grad_enabled(False):
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)

        running_corrects += torch.sum(preds == labels.data)

    accuracy = running_corrects.double() / dataset_sizes['val']
    print(f'Validation Accuracy: {accuracy:.4f}')

if __name__ == "__main__":
    # Set device
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Define transformations for the validation set
    data_transforms = {
        'val': transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ]),
    }

    # Define data directory
    data_dir = 'sign_split'
    image_datasets = {'val': datasets.ImageFolder(os.path.join(data_dir, 'val'), data_transforms['val'])}
    dataloaders = {'val': DataLoader(image_datasets['val'], batch_size=32, shuffle=True, num_workers=4)}
    dataset_sizes = {'val': len(image_datasets['val'])}
    class_names = image_datasets['val'].classes

    # Load the saved model
    model_ft = models.resnet18(pretrained=False)
    num_ftrs = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_ftrs, len(class_names))
    model_ft.load_state_dict(torch.load('resnet18_stop_priority1.pth'))
    model_ft = model_ft.to(device)

    # Evaluate the model
    evaluate_model(model_ft, dataloaders, dataset_sizes, device)
