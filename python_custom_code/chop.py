import subprocess
import os
def gdalsubprocess( path, file, outp, outn, padding, startx, starty ):
        
        cmd = f'C:\\OSGeo4W\\bin\\gdal_translate -srcwin {startx} {starty} {padding} {padding} {path}\{file} {outp}\{outn}'
        print(cmd)
        
        subprocess.run(cmd,shell=True)

path=r"E:\\detect_data\\wind_turbi_test_data_001_ongeknipt"
outp = r"E:\\detect_data\\wind_turbi_test_data_001"

for file in os.listdir(path):
    startx=0
    starty=0
    padding = 1280 
    starty=0
    for i in range(round(12500/1280)*round(12500/1280)):
            outn = f"{file[:-4]}patch_"+str(i)+".tif"

            if startx+1280 > 12500+1280:
                   starty += 1280
                   startx = 0

            gdalsubprocess(path, file, outp, outn, padding, startx, starty)
            startx+=1280










            
# import numpy as np
# from patchify import patchify
# from PIL import Image
# import cv2

# #converts image into a numpy array
# ocean = np.array(Image.open(r"C:\Users\Rik\Downloads\wind_turbi_test_data\2022_120000_513000_RGB_hrl.tif")) #612 X 408
# print('array:: windturbine\n')
# print(ocean)
# print('shape:: windturbine\n')
# print(ocean.shape)
# # ocean = np.asarray(ocean)
# # print('asarray:: ocean\n')
# # print(ocean)


# patches = patchify(ocean, (1280, 1280, 3), 1280)
# print(patches.shape)
# for i in range(patches.shape[0]):
#     for j in range(patches.shape[1]):
#         patch = patches[i, j, 0]
#         patch = Image.fromarray(patch)
#         num = i * patches.shape[1] + j
#         patch.save(f"patch_{num}.tif")



            