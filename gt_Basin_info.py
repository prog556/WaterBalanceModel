# creates zipped shapefile
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
#*******************************************************************************
# code summary
#1 - gets latitude, basin area from shapefile
#2 - gets monthly, daily streamflow
import arcpy, os, zipfile,glob,sys,numpy
from arcpy import env
arcpy.env.overwriteOutput=True
#*******************************************************************************
def basin_info(gageid, gageSHP,wkdir):
    if arcpy.Exists(gageSHP)=='FALSE':
         print 'shapefile does not exist'
    else:
        print 'shapefile exists'

        # copy shapefile to /in/ folder directory
        nameSHP = gageSHP.split('/')[-1]
        arcpy.CopyFeatures_management(gageSHP,wkdir+'/in/'+nameSHP)

        # get area of the catchment in sq km
        area=[row[0] for row in arcpy.da.SearchCursor(gageSHP,["SHAPE@AREA"])]
        areakm2 = float(area[0]/1000000)

        # output shapefile (in NAD83 DD)
        gageDD =wkdir+r'/in/G06746095_DD.shp'
        # point shapefile of basin centroids
        gageXY =wkdir+r'/in/G06746095_XY.shp'
        # coordinate system to project to
        in_spatial_ref = os.path.join(arcpy.GetInstallInfo()["InstallDir"], "Coordinate Systems/USGS_Favorites/North American Datum 1983.prj")
        # project original shapefile to DD
        arcpy.Project_management (gageSHP, gageDD, in_spatial_ref)
        # get internal centroid of basinDD
        arcpy.FeatureToPoint_management(gageDD,gageXY,"INSIDE")
        # add xy to centroid
        arcpy.AddXY_management(gageXY)
        lat=([row[0] for row in arcpy.da.SearchCursor(gageXY,["POINT_Y"])])[0]

        # name of zip file has a _z appended
        hruZipFile = wkdir+"/in/G06746095_z.zip"
        # fuction for creating zipped file
        zipShapefile(gageSHP,hruZipFile)
        print "HRU shapefile zipped up"

        # delete other files
        xfiles=[gageXY,gageDD]
        for x in xfiles:
            arcpy.Delete_management(x)

        # opens user input file (see WBM folder directory) and adds
        # in user inputs
        # \in\ locatin refers to the folder hierarchy for WBM-R
        # we can create our own file if necessary
        userinputs_orig = open(wkdir+'\in\user_input.txt','r')
        userlines = userinputs_orig.readlines()
        userinputs_orig.close()
        userinputs = open(wkdir+'\in\user_input.txt','w')
        inputlines = gageid+' '+str(lat)+'    '+str(areakm2)+'\n'
        userlines[7]=inputlines
        userinputs.writelines(userlines)
        userinputs.close()

if __name__ == '__main__':
    #  set parameters
    gageid = '06746095'
    gageSHP = r'D:/abock/temp/G06746095.shp'
    wkdir = r'D:/abock/Water_Balance/MWBM_test'

    # global wkdir?
    basin_info(gageid, gageSHP,wkdir)