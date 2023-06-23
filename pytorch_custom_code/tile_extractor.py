from haishoku.haishoku import Haishoku
import arcpy, os
from arcpy.ia import *
import subprocess

# first use the following command to make a vrt raster from the 4 terabytes of imagery
'''C:\OSGeo4W>gdalbuildvrt E:\stacked_raster.vrt E:\turbi_SAT\*.tif'''

AOI = r"E:\turbi_dataset\detecteer_data\turbi_laag.shp"
spatial_ref_poly = arcpy.Describe(AOI).spatialReference

def main():
    arcpy.env.overwriteOutput = True
    nid = 0
    # inputs
    fc_in = AOI
    width = 51.2 # with of the output rectangle
    height = 51.2 # height of the output rectangle

    # output
    fc_out = r'C:\Users\Rik\Documents\python_script\pytorch_custom_code\arcpy_workspace\object_in_tile_check\object_in_tile_check.gdb\rectangles_prod'

    # create empty output featureclass
    sr = arcpy.Describe(fc_in).spatialReference
    out_ws, out_name = os.path.split(fc_out)
    arcpy.CreateFeatureclass_management(out_ws, out_name, "POLYGON", fc_in, "DISABLED", "DISABLED", sr)

    # make fields list
    flds_use = correctFieldList(arcpy.ListFields(fc_in))

    # create insert cursor
    with arcpy.da.InsertCursor(fc_out, flds_use) as curs_out:

        # loop through input features
        with arcpy.da.SearchCursor(fc_in, flds_use) as curs_in:
            for row_in in curs_in:
                nid+=1
                polygon = createRectangleFromPoint(row_in[0].firstPoint, width, height, sr)
                row_out = buildRow(row_in, flds_use, polygon)
                curs_out.insertRow(row_out)
                arcpy.management.CopyFeatures(polygon, rf"C:\Users\Rik\Documents\python_script\pytorch_custom_code\arcpy_workspace\minipolys\{str(nid)}polypart.shp")
                poly = rf"C:\Users\Rik\Documents\python_script\pytorch_custom_code\arcpy_workspace\minipolys\{str(nid)}polypart.shp"
                gdalsubprocess( poly , nid )

def createRectangleFromPoint(pnt, width, height, sr):
    arrPnts = arcpy.Array()
    
    pnt2 = arcpy.Point(pnt.X - width, pnt.Y - height)
    arrPnts.add(pnt2)
    pnt2 = arcpy.Point(pnt.X - width, pnt.Y + height)
    arrPnts.add(pnt2)
    pnt2 = arcpy.Point(pnt.X + width, pnt.Y + height)
    arrPnts.add(pnt2)
    pnt2 = arcpy.Point(pnt.X + width, pnt.Y - height)
    arrPnts.add(pnt2)

    return arcpy.Polygon(arrPnts, sr) 

def correctFieldList(flds):
    flds_use = ['Shape@']
    
    fldtypes_not = ['Geometry', 'Guid', 'OID']
    for fld in flds:
        if not fld.type in fldtypes_not:
            flds_use.append(fld.name)
    return flds_use

def buildRow(row_in, flds_use, polygon):
    # try:
    lst_in = list(row_in)
    lst_in[0] = polygon

    return tuple(lst_in)


def gdalsubprocess( polygon, nid ):


        cmd = f'C:\\OSGeo4W\\bin\\gdalwarp.exe -cutline {polygon} -crop_to_cutline -dstnodata 0 "E:\\stacked_raster_1.vrt" "E:\\annoteer_materiaal_turbi_1\\vrt\\output00{str(nid)}.vrt" --config CHECK_DISK_FREE_SPACE FALSE'
        print(cmd)
        
        subprocess.run(cmd,shell=True)

        cmd = f'C:\\OSGeo4W\\bin\\gdal_translate.exe "E:\\annoteer_materiaal_turbi_1\\vrt\\output00{str(nid)}.vrt" "E:\\annoteer_materiaal_turbi_1\\tiff\\output00{str(nid)}.tif" --config CHECK_DISK_FREE_SPACE FALSE'
        print(cmd)
        
        subprocess.run(cmd,shell=True)

def remove_blacks(path):

    for filename in os.listdir(path):  
        image = path + '//' + filename
        dominant = Haishoku.getDominant( image )
        print(dominant, filename)
        if dominant == (0, 0, 0):
            os.remove(image)
    
if __name__ == '__main__':
    main()
    remove_blacks(r'E:\\annoteer_materiaal_turbi_1\\tiff')