# Gt_BasinInfo
# gets basin lat, basin area (sq. km), gageID (for streamflow)
# zips basin shapefile for pyGDP
# Import system modules
import arcpy, os, zipfile, glob
from arcpy import env
import numpy
arcpy.env.overwriteOutput=True

def trace():
    import os, sys, traceback
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    line = tbinfo.split(", ")[1]
    filename = sys.path[0] + os.sep + "1_WBM_main.py"
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror

# input shapefile (in albers/UTM)
gageSHP = r'D:/abock/temp/MWBM_test/in/G06746095.shp'

if arcpy.Exists(gageSHP)=='FALSE':
     print 'shapefile does not exist'
else:
    # get area of the catchment in sq km
    area=[row[0] for row in arcpy.da.SearchCursor(gageSHP,["SHAPE@AREA"])]
    areakm2 = float(area[0]/1000000)

    # output shapefile (in NAD83 DD)
    gageDD =r'D:/abock/temp/MWBM_test/in/G06746095_DD.shp'
    # point shapefile of basin centroids
    gageXY =r'D:/abock/temp/MWBM_test/in/G06746095_XY.shp'
    # coordinate system to project to
    in_spatial_ref = os.path.join(arcpy.GetInstallInfo()["InstallDir"], "Coordinate Systems/USGS_Favorites/North American Datum 1983.prj")
    # project original shapefile to DD
    arcpy.Project_management (gageSHP, gageDD, in_spatial_ref)
    # get internal centroid of basinDD
    arcpy.FeatureToPoint_management(gageDD,gageXY,"INSIDE")
    # add xy to centroid
    arcpy.AddXY_management(gageXY)
    lat=([row[0] for row in arcpy.da.SearchCursor(gageXY,["POINT_Y"])])[0]

    hruZipFile = "D:/abock/temp/MWBM_test/in/G06746095_z.zip"
    # fuction for creating zipped file
    def zipShapefile(inShapefile, newZipFN):
        print 'Starting to Zip '+inShapefile+' to '+newZipFN
        if not (os.path.exists(inShapefile)):
            print inShapefile + ' Does Not Exist'
            return False

        if (os.path.exists(newZipFN)):
            print 'Deleting '+newZipFN
            os.remove(newZipFN)

        if (os.path.exists(newZipFN)):
            print 'Unable to Delete'+newZipFN
            return False

        zipobj = zipfile.ZipFile(newZipFN,'w')

        for infile in glob.glob( inShapefile.lower().replace(".shp",".*")):
            print infile
            zipobj.write(infile,os.path.basename(infile),zipfile.ZIP_DEFLATED)
        zipobj.close()

        return True

    zipShapefile(gageSHP,hruZipFile)
    print "HRU shapefile zipped up"
    xfiles=[gageXY,gageDD]
    for x in xfiles:
        arcpy.Delete_management(x)






