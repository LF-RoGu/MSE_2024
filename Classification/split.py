import os
import shutil
import random

def split_dataset(dataset_dir, train_dir, val_dir, val_ratio=0.2):
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(val_dir):
        os.makedirs(val_dir)

    classes = os.listdir(dataset_dir)
    for cls in classes:
        cls_dir = os.path.join(dataset_dir, cls)
        images = os.listdir(cls_dir)
        random.shuffle(images)

        val_count = int(len(images) * val_ratio)
        train_images = images[val_count:]
        val_images = images[:val_count]

        train_cls_dir = os.path.join(train_dir, cls)
        val_cls_dir = os.path.join(val_dir, cls)
        os.makedirs(train_cls_dir, exist_ok=True)
        os.makedirs(val_cls_dir, exist_ok=True)

        for img in train_images:
            shutil.copy2(os.path.join(cls_dir, img), os.path.join(train_cls_dir, img))
        for img in val_images:
            shutil.copy2(os.path.join(cls_dir, img), os.path.join(val_cls_dir, img))

# Paths
dataset_dir = 'sign'
train_dir = 'sign_split/train'
val_dir = 'sign_split/val'

split_dataset(dataset_dir, train_dir, val_dir)
