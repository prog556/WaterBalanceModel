# dependencies OWSLIB, xmltree
import os,pyGDP,shutil
from datetime import date
import csv

# start on datsets 1,2,3,4,7 (#7 actually has 4 datasets within it)
# each dataset has its own properties
#   1 - dataset name
#   2 - thread server url
#   3- period of record
#   4 - name of precipitation variable
#   5 - name of temperature variable
#   6 - monthly/daily


#Current day for prism
current = date.day + date.month + date.year



Gridded_Observed_Data_1950_1999 = ['Gridded Observed Data(1950-1999)', 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml', 'Daily', '01/01/1950', '12/31/1999', 'Prcp', 'Tavg']
Gridded_Observed_Data_1949_2010 = ['Gridded Observed Data(1949-2010)', 'http://cida.usgs.gov/thredds/dodsC/new_gmo', 'Daily', '01/01/1949', '12/31/2010', 'Prcp', 'Tavg']
PRISM = ['PRISM', 'http://cida.usgs.gov/thredds/dodsC/prism', 'Monthly', '01/01/1985', current, 'Ppt', 'Tmx', 'Tmn']
DAYMET = ['DAYMET', 'dods://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet', 'Daily', '01/01/1980', '12/31/2011', 'Prcp', 'Tmax', 'Tmin']
MPI_ECHAM5 = ['MPI ECHAM5', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/EH5/merged/Monthly/RegCM3_Monthly_merged_EH5.ncml', 'Monthly', '01/16/1958', '12/16/2099', 'RT', 'TA']
GENMON = ['GENMON', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GENMOM/ena/Monthly/RegCM3_Monthly_merged_GENMOM.ncml', 'Monthly', '01/16/1980', '12/16/2089', 'RT', 'TA']
GFDL_CM_2_0 = ['GFDL CM 2.0', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GFDL/ena/Monthly/RegCM3_Monthly_merged_GFDL.ncml', 'Monthly', '01/16/1980', '12/16/2069', 'RT', 'TA']
NOAA_NCEP = ['NOAA NCEP', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/NCEP/ena/Monthly/RegCM3_Monthly_merged_NCEP.ncml','Monthly', '01/16/1982', '12/16/2007']

#List of a list of the properties for each dataset
data = [Gridded_Observed_Data_1950_1999, Gridded_Observed_Data_1949_2010, PRISM, DAYMET, MPI_ECHAM5, GENMON, GFDL_CM_2_0, NOAA_NCEP]

# link to region 6 hrus
pyGDP.WFS_URL = 'https://www.sciencebase.gov/catalogMaps/mapping/ows/51b0d374e4b030b519830d73'
# science base access:  https://my.usgs.gov/confluence/display/GeoDataPortal/pyGDP+FAQ
pyGDP = pyGDP.pyGDPwebProcessing()

"""
This example shows how to use multiple dataTypes and Statistics.

"""
# change working directory so the GDP output will be written there
#was originally in the D drive, but that is my Disk drive
os.chdir("C:\\Users\\reimandy\\Documents\\pyGDP")
# tile and dataset variables

## move out of loops
region = 'R06'
#dataset='MPI'
    
# create list of hru_ids that can be used for the uservalue
hruids = list(range(1,2304))
hruid_list=[]
for i in range(0,len(hruids)):
    hruid_list.append(str(hruids[i]))
    print 'list finished'
    
# get list of shapefiles uploaded to the GDP
shapefiles = pyGDP.getShapefiles()
for shp in shapefiles:
    print shp
    
# this will upload your file if it is not in GDP.
#shapefile='D://temp//R06a_hrus.zip'
#shape = pyGDP.uploadShapeFile(shapefile)
    
# in the future this will be loaded from SCienceBase
#shapefile='upload:nhru'
shapefile = 'sb:R06a_hru'
user_attribute = 'hru_id_loc'
# to summarize for a single fature
#user_value = '10'
# to summarize for all ids
user_value = hruid_list
# end of move out of loop

for dataset in data:

    print "The current dataset being worked on is: " + dataset[0]

    # link/variables name from the word documents
    #dataSets = ['http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/EH5/merged/Monthly/RegCM3_Monthly_merged_EH5.ncml',\
    #'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GENMOM/merged/Monthly/RegCM3_Monthly_merged_GENMOM.ncml']
    #dataSet='http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/EH5/merged/Monthly/RegCM3_Monthly_merged_EH5.ncml'
    
    #The url of each dataset
    dataSet = dataset[1]
    
    #The precipitation and temperatures of each dataset
    #Start at position(not index) 5 until the end of the 
    #dictionary's key(which is a list) 
    dataType=[dataset[6:]]
    
    # input arguments for extracting data
    # not sure how sensitive beginning/ending time are for monthly, data, guess we'll figure it out
    #timeBegin = '1980-01-01T00:00:00.000Z'
    #timeEnd = '1981-12-31T00:00:00.000Z'
   
    timeStep = dataset[2]
   
    #Start date 
    timeBegin = dataset[3]
    #End date
    timeEnd = dataset[4]
    gmlIDs=None
    verbose=True
    coverage='true'
    delim='COMMA'
    stats='MEAN'
    
    # run the pyGDP
    #loop through each list of dataSet
    outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    print outputPath
    # copy the output and rename it
    shutil.copy2(outputPath, region+'_'+dataset)
    
    #Parse the csv file into precip and temp
    index = 0

    csvread = csv.reader(open(outputPath + '.csv', "rb")) 
    csvwrite = csv.writer(open(dataType[0] + '.csv', "wb"))
    
    temp = csvread
    var = temp.next()
    #Gets gage ids
    gage = temp.next()
    
    for variable in dataType:
        
        #Writes current variable to csv file
        csvwrite.writerow(var)
        #Writes all gage ids to csv file
        csvwrite.writerow(gage)
        
        for row in csvread:
            
            #if on last variable     
            if variable == dataType[len(dataType) - 1]: 
                csvwrite.writerow(row)               
                try:
                    csvread.next()
                except StopIteration:
                    print "Finished Parsing the csv File"
                    
            else:  
                if row[0] in dataType[index+1]:
                    #Line 33 is used for titling the csv file the name of the variable (like tmin, ppt, or tmax)
                    var[0] = dataType[index+1]
                    csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                    break
                else:
                    csvwrite.writerow(row)
            
        # use index to keep track of next variable
        if (index + 1) < len(dataType):
            index += 1
    
    
    ##print 'Processing request.'
    ##for dataSet in dataSets:
    ##    print dataSet
    ##    # file exists on current file system in current working directory
    ##    outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    ##    # os.getcwd() append outputPath to working directory
    ##    print outputPath
    ##print 'finished'