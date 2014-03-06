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

# determines number of days between two dates
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

#*******************************************************************************
# code summary
#1 - gets latitude, basin area from shapefile
#2 - gets monthly, daily streamflow
import arcpy, os, zipfile,glob,sys,datetime,numpy
from datetime import datetime, date, timedelta, time
# need urllib to get streamflow data from NWIS (website parsing module)
import urllib
from arcpy import env
arcpy.env.overwriteOutput=True

#*************************************************************
# pick gage id
gageid = '06746095'
# input shapefile (in albers/UTM)
gageSHP = r'D:/abock/temp/G06746095.shp'
wkdir = r'D:/abock/Water_Balance/MWBM_test'
# pick the dates that you are interested in getting streamflow for
y0 = 1949
m0 = 1
y1 = 2012
m1 = 12
#*************************************************************
# produce start and end dates
if len(str(m0))==1:
    m0_str='0'+str(m0)
if len(str(m1))==1:
    m1_str='0'+str(m1)
else:
    m1_str = str(m1)
d0 = date(y0,m0,1)
d0_url = str(y0)+'-'+m0_str+'-01'
d1 = date(y1,m1,31)
d1_url = str(y1)+'-'+m1_str+'-31'

# check input data
# does shapefile exist, what projection is it in

#*******************************************************************************
if arcpy.Exists(gageSHP)=='FALSE':
     print 'shapefile does not exist'
else:
    print 'shapefile exists'

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
    userinputs_orig = open(wkdir+'\in\user_input.txt','r')
    userlines = userinputs_orig.readlines()
    userinputs_orig.close()
    userinputs = open(wkdir+'\in\user_input.txt','w')
    inputlines = gageid+' '+str(lat)+'    '+str(areakm2)+'\n'
    userlines[7]=inputlines
    userinputs.writelines()
    userinputs.close()

#*******************************************************************************
    years=[]
    months=[]
    days=[]

    # determine number of days between start/end of POR specified by user
    newdate=date(d1.year,d1.month,d1.day)+timedelta(1)
    for result in perdelta(d0, newdate, timedelta(days=1)):
        dt = datetime.strptime(str(result), "%Y-%m-%d")
        t = dt.timetuple()
        years.append(t[0])
        months.append(t[1])
        days.append(t[2])

    # make empty matrix for holding daily flow data, the length of the matrix
    # is the number of days specified by user for POR
    delta = d0 - d1
    flows=numpy.zeros(shape=(abs(delta.days)+1,4))
    # -999 -> null/dummy value
    flows.fill(-999)
    flows[...,0]=years
    flows[...,1]=months
    flows[...,2]=days

    print 'Going to the NWIS web services for each gage.'
    # these are codes that explain where there streamgage data did not meet
    # the QA/QC check
    noDataList=['Ice','Eqp','Bkw','Rat','Dis','Ssn','Mnt','***']

    # get streamgage name, can get other station properties this way too.
    gagepage = urllib.urlopen('http://waterdata.usgs.gov/nwis/inventory?search_site_no='+gageid+'&search_site_no_match_type=exact&group_key=NONE&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&list_of_search_criteria=search_site_no')
    for line in gagepage:
        if len(line)>1:
            if line[3:13]=='station_nm':
                line = line.replace(' <station_nm>','')
                line = line.replace('</station_nm>\n','')
                if line !=' ':
                    Sta_name=line

    # get daily streamflow from NWIS
    # codes 0.00_ZFl, Zfl - zero flow
    usock = urllib.urlopen('http://waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='+gageid+'&search_site_no_match_type=exact&site_tp_cd=ST&index_pmcode_30208=1&index_pmcode_00060=1&index_pmcode_99060=1&sort_key=site_no&group_key=NONE&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='+str(d0_url)+'&end_date='+str(d1_url)+'&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection')
    dateList=[]
    flowList=[]
    count=0
    for line in usock:
        if line !='\n':
            items = line.split()
        if items[0]=='USGS':
            dateList.append(items[2])
            if len(items)<4:
                flowList.append(-999)
            else:
                if items[3]=='0.00_ZFl':
                    flowList.append(0)
                if items[3]=='ZFl':
                    print 'ZFl'
                    flowList.append(0)
                elif items[3] in noDataList:
                    flowList.append(-999)
                else:
                    flowList.append(items[3])
    # convert strings to float
    # this may throw an exception if there is a QAQC code (aka line 146) that has slipped through
    flowList_float=[float(x) for x in flowList]

    # this piece of code places the streamflow data into the matrix
    # this is important because the streamflow data may begin/end inside matrix
    if len(dateList)>0:
        first_day=dateList[0].split('-')
        date_integer=[int(x) for x in first_day]
        date_format = date(date_integer[0],date_integer[1],date_integer[2])
        delta = d0 - date_format
        #print delta.days
        if delta.days!=0:
            placer = abs(delta.days)
        if delta.days==0:
            placer=0
        len(flowList_float)
        print placer
        x=flowList_float.count(-999.0)
        flows[placer:len(flowList_float)+placer,3]=flowList_float
    else:
        flows[...,i]=-999
    flows[flows==-999.0]=numpy.nan
    # save to daily textfile
    numpy.savetxt(wkdir+r'/in/Flows_daily.txt', flows, fmt='%s',delimiter=' ')

    #convert from daily cfs to monthly (mm)
    streamflowfile= open(wkdir+r'/in/Flows_monthly.txt','w')
    for i in range(min(years),max(years)+1):
        for j in range(1,13):
            month=flows[(flows[:,0]==i)&(flows[:,1]==j)]
            mask_month = numpy.ma.masked_array(month[:,3],numpy.isnan(month[:,3]))
            #arr = numpy.ma.array(0,flows,1)
            if (numpy.ma.max(mask_month)is numpy.ma.masked)==False:
                month_mean=numpy.mean(mask_month)
                month_mean_mm=((month_mean/float(areakm2))*2.446514*len(mask_month))
                month_mean_mm=round(month_mean_mm,2)
            else:
                month_mean_mm='NA'
            #print month_mean
            newline = str(years[i])+' '+str(j)+' '+str(month_mean_mm)+'\n'
            streamflowfile.writelines(newline)
    streamflowfile.close()
