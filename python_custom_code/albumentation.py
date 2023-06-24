import os
import cv2
import albumentations as A
from PIL import Image as im
import numpy as np
# Define the path to the input directory containing the images
input_dir = "C:\\datasets\\windturbine\\traindata_backup\\images"

# Define the path to the output directory where augmented images will be saved
output_dir = "C:\\datasets\\windturbine\\traindata_backup\\images_augmented"
output_annotation_path = "C:\\datasets\\windturbine\\traindata_backup\\labels_augmented"
bbxes = []
cl_nr = []
# Define the augmentation transformations you want to apply
transform = A.Compose([
    A.OneOf([
        A.RandomCrop(896,896,p=0.7),
        A.RandomSizedBBoxSafeCrop(896,896,p=0.3),
    ], p=1.0),
    A.OneOf([
        A.ElasticTransform(p=0.3,alpha=4,sigma=50),
        A.GridDistortion(p=0.3, num_steps=5, distort_limit=0.3),
    ], p=1.0),
    A.OneOf([
        A.ToGray(p=0.6),
        A.RandomBrightnessContrast(p=0.6),
    ], p=1.0),
    A.Flip(always_apply=True)
    # Add more desired transformations here
],  bbox_params=A.BboxParams(format="yolo", label_fields=[]))


# Iterate over the images in the input directory
for filename in os.listdir(input_dir):
    box = []
    cl_nr = []
    with open(input_dir[:-6]+"labels"+"\\"+filename[:-4]+".txt", "r") as f:
        for line in f:
            test_txt = line.split(" ")
            
            if int(test_txt[0])==0:
                n=0
            if int(test_txt[0])==1:
                n=1
            box = [float(test_txt[1]),float(test_txt[2]),float(test_txt[3]),float(test_txt[4])]
            print(box)
            cl_nr.append(n)
            bbxes.append(box)
            
    image_path = os.path.join(input_dir, filename)

    if os.path.isfile(image_path):

        # Load the image
        image = im.open(image_path)
         

        image = np.array(image)
        # Apply the augmentation transformations
        augmentation = transform(image=image, bboxes=bbxes)
        augmented_image = augmentation["image"]
        augmented_bbx = augmentation["bboxes"]
        # Save the augmented image to the output directory
        output_path = os.path.join(output_dir, f"augmented_{filename}")
        cv2.imwrite(output_path, augmented_image)
        


        with open(output_annotation_path+"//"+f"augmented_{filename[:-4]}.txt", "w") as f:
            for bbox, cl_nr in zip(augmented_bbx, cl_nr):
                f.write(f"{cl_nr} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")

