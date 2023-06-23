import glob, os
import shutil

tr_obj_dir = r"C:\datasets\windturbine\train\img"
tr_lbl_dir = r"C:\datasets\windturbine\train\anno"
val_obj_dir =  r"C:\datasets\windturbine\valid\img"
val_lbl_dir = r"C:\datasets\windturbine\valid\anno"
# Percentage of images to be used for the test set
percentage_test = 10


# Populate train.txt and test.txt
counter = 1
index_test = round(100 / percentage_test)
for i in glob.iglob(os.path.join(tr_obj_dir, "*.tif")):
    title, ext = os.path.splitext(os.path.basename(i))

    if counter == index_test:
        counter = 1
        shutil.move(tr_obj_dir + "\\" + title + '.tif', val_obj_dir + "\\" + title + '.tif')
        shutil.move(tr_lbl_dir + "\\" + title + '.txt', val_lbl_dir + "\\" + title + '.txt')
    else:
        counter = counter + 1