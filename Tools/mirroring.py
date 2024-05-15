import os
from PIL import Image, ImageOps

def parse_filename(filename):
    # Split the filename to extract x and y coordinates
    base_name = os.path.splitext(filename)[0]
    parts = base_name.split('_')
    if len(parts) >= 3:
        x = int(parts[0])
        y = int(parts[1])
        suffix = '_'.join(parts[2:])
        return x, y, suffix
    else:
        raise ValueError("Filename does not match the expected pattern")

def construct_new_filename(new_x, y, suffix, extension):
    # Create a new filename with updated x coordinate
    new_filename = f'{new_x}_{y}_{suffix}{extension}'
    return new_filename

def mirror_image(image):
    return ImageOps.mirror(image)

def process_dataset(images_dir):
    output_images_dir = os.path.join(images_dir, 'mirrored_images')
    
    if not os.path.exists(output_images_dir):
        os.makedirs(output_images_dir)
    
    for filename in os.listdir(images_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            try:
                print(f"Processing file: {filename}")
                x, y, suffix = parse_filename(filename)
                
                image_path = os.path.join(images_dir, filename)
                image = Image.open(image_path)
                
                mirrored_image = mirror_image(image)
                new_x = image.width - x
                
                new_filename = construct_new_filename(new_x, y, suffix, os.path.splitext(filename)[1])
                mirrored_image.save(os.path.join(output_images_dir, new_filename))
                print(f"Saved mirrored image as: {new_filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

# Define the current directory
images_dir = os.getcwd()

# Process the dataset
process_dataset(images_dir)
