from osgeo import osr, ogr, gdal
import os
from shapely.geometry import mapping, Polygon
from shapely.ops import unary_union
import fiona
import geopandas as gpd

cnt = 0
polylist = []
confv = []

def pixel_to_world(geo_matrix, x, y):
    ul_x = geo_matrix[0]
    ul_y = geo_matrix[3]
    x_dist = geo_matrix[1]
    y_dist = geo_matrix[5]
    _x = x * x_dist + ul_x
    _y = y * y_dist + ul_y
    return _x, _y


SCREEN_DIMENSIONS = (1280, 1280)
def xywh2xyxy_(x,y,w,h):
        x1, y1 = x-w/2, y-h/2
        x2, y2 = x+w/2, y+h/2
        return x1, y1, x2, y2

def xyxy2pixel_(coords):
    return tuple(round(coord * dimension) for coord, dimension in zip(coords, SCREEN_DIMENSIONS))
TEST_ANNO = r"C:\\yolov5\\runs\\detect\\exp4\\labels"
for i in os.listdir(TEST_ANNO):

    

    with open((r"C:\\yolov5\\runs\\detect\\exp4\\labels\\"+i), "r") as test_txt:
        for line in test_txt:
            test_txt = line.split(" ")
            
            if int(test_txt[0])==0:

                xyxy = xywh2xyxy_(float(test_txt[1]),float(test_txt[2]),float(test_txt[3]),float(test_txt[4]))
                XminYmin = (xyxy[0],xyxy[1])
                XmaxYmax= (xyxy[2],xyxy[3])

                XminYmax = (xyxy[0],xyxy[3])
                XmaxYmin = (xyxy[2],xyxy[1])


    # convert xyxy coords to pixel values:
                xmin=(xyxy2pixel_(XminYmin)[0])
                ymin=(xyxy2pixel_(XminYmin)[1])
                xmax=(xyxy2pixel_(XmaxYmax)[0])
                ymax=(xyxy2pixel_(XmaxYmax)[1])
                


                ds = gdal.Open(r"E:\\detect_data\\wind_turbi_test_data_000\\"+i[:-4]+".tif")

                world_Xmin, world_Ymin = pixel_to_world(ds.GetGeoTransform(), xmin, ymin)
                world_Xmax, world_Ymax = pixel_to_world(ds.GetGeoTransform(), xmax, ymax)
                world_Xmin, world_Ymax = pixel_to_world(ds.GetGeoTransform(), xmin, ymax)
                world_Xmax, world_Ymin = pixel_to_world(ds.GetGeoTransform(), xmax, ymin)

                coord1 = (world_Xmax, world_Ymax)
                coord2 = (world_Xmax, world_Ymin)
                coord3 = (world_Xmin, world_Ymin)
                coord4 = (world_Xmin, world_Ymax)

        # Here's an example Shapely geometry
                poly = Polygon([coord1, coord2, coord3, coord4])
                polylist.append(poly)
                confv.append(float(test_txt[5]))
                print(len(polylist)," ",len(confv))
                # Define a polygon feature geometry with one attribute
    
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int',
                       'confv':'float'},
    }

    # Write a new Shapefile
    
    with fiona.open(f'E:\\python_script\\gisified_results\\square_bbxs_turb2_conf.shp', 'w', 'ESRI Shapefile', schema) as c:
        ## If there are multiple geometries, put the "for" loop here
        for i, cnf in zip(polylist, confv):
            cnt+=1
            c.write({
                'geometry': mapping(i),
                'properties': {'id': cnt,
                               'confv': cnf},
            })

    
    # GeoDataFrame creation
    poly = gpd.read_file("E:\\python_script\\gisified_results\\square_bbxs_turb2_conf.shp")
    points = poly.copy()
    points.geometry = points['geometry'].centroid
    # same crs
    points.crs=poly.crs
    # save the shapefile
    points.to_file('E:\\python_script\\gisified_results\\bbxs_centroid_turb2_conf.shp')


    