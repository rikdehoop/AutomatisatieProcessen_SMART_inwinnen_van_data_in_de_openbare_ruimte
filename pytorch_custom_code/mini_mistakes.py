import subprocess
import os
def gdalsubprocess( shp_name, shp_filepath, tif_path, file):
        
        cmd = f'''C:\\OSGeo4W\\bin\\gdal_rasterize -b 1 -b 2 -b 3 -burn 0 -burn 0 -burn 0 -l {shp_name} {shp_filepath} {tif_path + "//" + file}'''
        print(cmd)
        
        subprocess.run(cmd,shell=True)
tif_path = r'E:\\detect_data\\wind_turbi_test_data_000'
shp_filepath = r"E:\\Data\\uitslutinggebieden\\kunststof_sportvelden_.shp"
shp_name = os.path.split(shp_filepath)
for file in os.listdir(tif_path):
            gdalsubprocess(shp_name[1][:-4], shp_filepath, tif_path,file)
