import os
import shutil
import cv2
import pandas as pd
#check which images match the annotation name 
def rename_files(dir="train"):
    nn = 0
    #rename names to a more readable normalized title:
    for i in os.listdir(dir):
        if i.endswith(".tif"):
            im = i
            continue
        if i.endswith(".txt"):
            if i[:-4] == im[:-4]:
                nn += 1
                n = f"{nn}"
                n = n.zfill(10)
                os.rename(f"{dir}//{im}",f"{dir}//{n}.tif")
                os.rename(f"{dir}//{i}",f"{dir}//{n}.txt")
            else: print("nope")

def if_match_move(im_path="images", anno_path="annotations", out="train"):
    imgdir = im_path
    annodir = anno_path
    annolist = []
    count = 0
    # Write annotation names to list
    for i in os.listdir(annodir):
        # checking if it is a file
        count += 1
        if i.endswith('.txt') and os.path.isfile(annodir+"\\"+i): 
            annolist.append(i[:-4])
    print(count)
    print(len(annolist))

    count = 0
    #   Check if images in annotation and move
    for i in os.listdir(imgdir):
        if i.endswith('.tif') and os.path.isfile(imgdir+"\\"+i):
            if i[:-4] in annolist:
                count += 1
                shutil.move(imgdir+"\\"+i, out)
                shutil.move(annodir+"\\"+i[:-4]+".txt", "train/anno")
        
    print(count)


# if_match_move(im_path=r"C:\Users\Rik\Downloads\wind_turbi_data", anno_path=r"C:\Users\Rik\Downloads\wind_turbi_data", out="train/img")

# convert xmin, xmax, ymin, ymax 2 x-center, y-center, width , height
def yolo_xywh_(xmax, xmin, ymax, ymin, tot_xmax, tot_ymax): 
    yolo_xywh = ((xmax+xmin)/2)/tot_xmax, ((ymax+ymin)/2)/tot_ymax, (xmax-xmin)/tot_xmax, (ymax-ymin)/tot_ymax
    return yolo_xywh


# Writes new annotation files from csv to txt whith matching image names 
# pd.set_option('display.max_columns', None) 
# pd.set_option('display.max_colwidth', None)  # or 199
# df = pd.read_csv('lbborkowski wind-turbine-detector master annotations//train_labels.csv')
# df['class'] = df['class'].replace('wind turbine','0')
# print(len(df.index))
# for i in range(len(df.index)):
#     with open(f"train//{str(df.loc[i,'filename'])[:-4]}.txt", 'w') as my_file:
#         xmax = int(df.loc[i,'xmax'])
#         xmin = int(df.loc[i,'xmin'])
#         tot_xmax = 300
#         ymax = int(df.loc[i,'ymax'])
#         ymin = int(df.loc[i,'ymin'])
#         tot_ymax = 300

#         yolo_xywh = yolo_xywh_(xmax, xmin, ymax, ymin, tot_xmax, tot_ymax)

#         # write new files
#         my_file.write(str(df.loc[i,'class']) + " " + str(yolo_xywh[0])  + " " +  str(yolo_xywh[1])  + " " +  str(yolo_xywh[2])  + " " +  str(yolo_xywh[3]) + "\n")

#         # move image files
# for i in os.listdir('lbborkowski wind-turbine-detector master images//train'):
#     if i.endswith('.jpg'):
#         shutil.move(f'lbborkowski wind-turbine-detector master images//train//{i}', f"train//{i}")



import glob, os
import shutil
import cv2    
TEST_IMGAGE = r"C:\\datasets\\windturbine\\train\\labels\\augmented_0000000003.tif"
# convert xywh coords to xyxy coords

    
def xywh2xyxy_(x,y,w,h):
        x1, y1 = x-w/2, y-h/2
        x2, y2 = x+w/2, y+h/2
        return x1, y1, x2, y2




with open((TEST_IMGAGE[:-4]+".txt"), "r") as test_txt:
    test_txt = test_txt.readlines()[0].split(" ")

xyxy = xywh2xyxy_(float(test_txt[1]),float(test_txt[2]),float(test_txt[3]),float(test_txt[4]))
XminYmin = (xyxy[0],xyxy[1])
XmaxYmax= (xyxy[2],xyxy[3])

XminYmax = (xyxy[0],xyxy[3])
XmaxYmin = (xyxy[2],xyxy[1])
print(xyxy)




# convert xyxy coords to pixel values:
SCREEN_DIMENSIONS = (1279, 1279)

def xyxy2pixel_(coords):
    return tuple(round(coord * dimension) for coord, dimension in zip(coords, SCREEN_DIMENSIONS))

#check if annotations are correctly matched with images:
def check_annotations(img_in=TEST_IMGAGE):

    # Reading an image in default mode
    image = cv2.imread(img_in)
    # Window name in which image is displayed
    window_name = 'Image'

    # represents the top left corner of rectangle
    start_point = xyxy2pixel_(XminYmin)

    # represents the bottom right corner of rectangle
    end_point = xyxy2pixel_(XmaxYmax)
    # Blue color in BGR
    color = (255, 0, 0)
    # Line thickness of 2 px
    thickness = 2

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    image = cv2.rectangle(image, start_point, end_point, color, thickness)

    # Displaying the image 
    imS = cv2.resize(image, (540, 540)) 
    cv2.imshow(window_name, imS) 
    k = cv2.waitKey(0)
    if k==ord('q'):
        cv2.destroyAllWindows()



# for i in os.listdir(r"C:\\datasets\\windturbine\\train\\labels"):
#     if os.stat(r"C:\\datasets\\windturbine\\train\\labels\\" +i).st_size == 0:
#         print("empty")
#         print(i)

check_annotations(r"C:\\datasets\\windturbine\\train\\images\\augmented_0000000003.tif")

def delete_class():

    for i in os.listdir(r"C:/datasets/propaan/train/labels"):


        with open(r"C:\\datasets\\propaan\\train\\labels\\"+ i, "r") as input:
            with open(r"C:\datasets\propaan\train\lables1\temp.txt", "w") as output:
                # iterate all lines from file
                for line in input:
                    # if line starts with substring 'time' then don't write it in temp file
                    if not line.strip("\n").startswith('1'):
                        output.write(line)

        # replace file with original name
        os.replace(r"C:\datasets\propaan\train\lables1\temp.txt", i)
    
