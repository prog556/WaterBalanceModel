# dependencies OWSLIB, xmltree
import os,pyGDP,shutil, time

global csvfile, vistrails_data_set, nhru, url

def main_func(curdir, data_set, region):
    
    def Region_lookup(region):
        region_properties = []
        
        if region == 'nhru':
            region_properties.append(371)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d35da1e4b0ca184833940c')
            region_properties.append('false')
        elif region == 'R01':
            region_properties.append(2462)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5244735ae4b05b217bada04e')
            region_properties.append('false')
        elif region == 'R02':
            region_properties.append(4827)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52696784e4b0584cbe9168ee')
            region_properties.append('false')
        elif region == 'R03':
            region_properties.append(9899)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5283bd23e4b047efbbb57922')
            region_properties.append('false')
        elif region == 'R04':
            region_properties.append(5936)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5284ff57e4b063f258e61b9d')
            region_properties.append('false')
        elif region == 'R05':
            region_properties.append(7182)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/528516bbe4b063f258e62161')
            region_properties.append('false')
        elif region == 'R06':
            region_properties.append(2303)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d75296e4b055e0afd5be2c')
            region_properties.append('true')
        elif region == 'R07':
            region_properties.append(8205)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52851cd5e4b063f258e643dd')
            region_properties.append('true')
        elif region == 'R08':
            region_properties.append(4449)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52854695e4b063f258e6513c')
            region_properties.append('true')
        elif region == 'R10L':
            region_properties.append(8603)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/520031dee4b0ad2d97189db2')
            region_properties.append('true')
        elif region =='R10U':
            region_properties.append(10299)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5216849ee4b0b45d6ba61e2e')
            region_properties.append('false')
        elif region == 'R11':
            region_properties.append(7373)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d1f9ebe4b08b18a62d586b')
            region_properties.append('true')
        elif region == 'R12':
            region_properties.append(7815)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5201328ae4b009d47a4c247a')
            region_properties.append('false')
        elif region == 'R13':
            region_properties.append(1958)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d752b9e4b055e0afd5be36')
            region_properties.append('false')
        elif region == 'R14':
            region_properties.append(3879)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52029c68e4b0e21cafa4b40c')
            region_properties.append('false')
        elif region == 'R15':
            region_properties.append(3441)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5285389ae4b063f258e64863')
            region_properties.append('false')
        elif region == 'R16':
            region_properties.append(2664)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52853f97e4b063f258e64875')
            region_properties.append('false')

        return region_properties

    def list_define(data_set):    
        if data_set == 'PRISM':
            return ['PRISM', 'http://cida.usgs.gov/thredds/dodsC/prism', 'Monthly', '2010-01-01T00:00:00.000Z', '2012-12-31T00:00:00.000Z', 'ppt', 'tmx', 'tmn']
        elif data_set == 'MPI_ECHAM5':
            return ['MPI ECHAM5', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/EH5/merged/Monthly/RegCM3_Monthly_merged_EH5.ncml', 'Monthly', '1968-01-01T00:00:00.000Z', '2099-12-31T00:00:00.000Z', 'RT', 'TA']
        elif data_set == 'GENMON':
            return ['GENMON', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GENMOM/merged/Monthly/RegCM3_Monthly_merged_GENMOM.ncml', 'Monthly', '1980-01-01T00:00:00.000Z', '2089-12-31T00:00:00.000Z', 'RT', 'TA'] 
        elif data_set == 'GFDL_CM_2_0':
            return ['GFDL CM 2.0', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GFDL/merged/Monthly/RegCM3_Monthly_merged_GFDL.ncml', 'Monthly', '1970-01-01T00:00:00.000Z', '2069-12-31T00:00:00.000Z', 'RT', 'TA']
        elif data_set == 'NOAA_NCEP':
            return ['NOAA NCEP', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/NCEP/merged/Monthly/RegCM3_Monthly_merged_NCEP.ncml','Monthly', '1982-01-01T00:00:00.000Z', '2007-12-31T00:00:00.000Z','RT','TA']
        elif data_set == 'GSD':
            return ['Gridded Observed Data(1949-2010)', 'http://cida.usgs.gov/thredds/dodsC/new_gmo', 'Daily', '1949-01-01T00:00:00.000Z', '2010-12-31T00:00:00.000Z', 'pr', 'tas']
        elif data_set == 'DAYMET':
            return ['DAYMET', 'dods://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet', 'Daily', '2010-01-01T00:00:00.000Z', '2012-01-01T00:00:00.000Z', 'prcp', 'tmax', 'tmin']
        elif data_set == 'Idaho':
            return ['Idaho','http://cida.usgs.gov/thredds/dodsC/UofIMETDATA','Daily','1979-01-01T00:00:00.000Z','2013-01-01T00:00:00.000Z','precipitation_amount','min_air_temperature','max_air_temperature']
    
    global csvfile, vt_dataset, nhru, length, vt_datatype, url
    import pyGDP
        
    Region_return=Region_lookup(region)
    hrus = Region_return[0]
    nhru = hrus
    ScienceBase_URL= Region_return[1]
    
    #NHDplus region
    
    # link to region 6 hrus on ScienceBase

    pyGDP.WFS_URL = ScienceBase_URL
    url = pyGDP.WFS_URL
    pyGDP = pyGDP.pyGDPwebProcessing()
    
    # change working directory so the GDP output will be written there
    
    
    # Datasets and their properties
    #**********************************
    #Gridded_Observed_Data_1950_1999 = ['Gridded Observed Data(1950-1999)', 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml', 'Daily', '1950-01-01T00:00:00.000Z', '1999-12-31T00:00:00.000Z', 'Prcp', 'Tavg']
       
    #data = [PRISM]#,MPI_ECHAM5,GENMON,GFDL_CM_2_0,NOAA_NCEP,GSD,DAYMET]
    #prism starts at 1895
    
    # get list of shapefiles uploaded to the GDP
    shapefiles = pyGDP.getShapefiles()
    for shp in shapefiles:
        print shp
    
    # feature loaded from sciencebase
    #shapefile = 'sb:'+region+'_hru'
    shapefile = 'sb:nhru'
    user_attribute = 'hru_id_loc'
    user_value = None
    
    #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\SBDDS')
    os.chdir(curdir)
    dir = os.getcwd()
    vt_data = list_define(data_set)
    vt_datatype = vt_data[5:]
             
    timestart = time.time()
    file_loc = curdir+'\\'+data_set
    if not os.path.exists(file_loc):
        os.mkdir(file_loc)
    os.chdir(file_loc)
    print "The current dataset being worked on is: " + data_set

    #The url of each dataset
    dataSet = vt_data[1]

    #The precipitation and temperatures of each dataset
    #Start at position(not index) 5 until the end of the
    #dictionary's key(which is a list)
    dataType=vt_data[5:]

    # daily or monthly for additional aggregation/formatting (not appended yet)
    timeStep = vt_data[2]
    #Length is for connecting to vistrails
    length = timeStep

    #Start date
    timeBegin = vt_data[3]
    #End date
    timeEnd = vt_data[4]

    # data processing arguments
    gmlIDs=None
    verbose=True
    #coverage = 'false' check if on US border/ocean
    
    coverage = Region_return[2]
    delim='COMMA'
    stats='MEAN'

    # run the pyGDP
    start = time.time()
    outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    end = time.time()
    print 'Start time is: ' + str(start)
    print 'End time is: ' + str(end)
    print 'Total time was: ' + str(end-start)
    print outputPath
    # copy the output and rename it
    shutil.copy2(outputPath, region+'_'+vt_data[0]+'.csv')
    
#         #Parse the csv file 
#         index = 0
#             
#         csvread = csv.reader(open(region+'_'+dataset[0] + '.csv', "rb")) 
#         csvwrite = csv.writer(open(dataType[0] + '.csv', "wb"))
#         
#         index = 0
#         
#         temp = csvread
#         var = temp.next()
#         #Gets gage ids
#         gage = temp.next()
#         
#         #Writes current variable to csv file
#         csvwrite.writerow(var)
#         #Writes all gage ids to csv file
#         csvwrite.writerow(gage)
#         
#         for variable in dataType:                
#                 
#             for row in csvread:
#                 #if on last variable     
#                 if variable == dataType[len(dataType) - 1]: 
#                     csvwrite.writerow(row)               
#                 else:  
#                     if (row[0] in '#'+dataType[index+1]) or (row[0] in '# '+dataType[index+1]):
#                         #Line 33 is used for titling the csv file the name of the variable (like tmin, ppt, or tmax)
#                         var = '#'+dataType[index+1]
#                         csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
#                         row[1:] = ""
#                         row[0] = var
#                         csvwrite.writerow(row)
#                         csvwrite.writerow(gage)
#                         
#                         if len(dataType) == 2:
#                             csvread.next()
#                         else:
#                             csvread.next()
#                             csvwrite.writerow(csvread.next())
#                             csvwrite.writerow(csvread.next())
#                         break
#                     else:
#                         if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
#                             csvwrite.writerow(row)
#             print "Finished parsing " + variable + ".csv"
#             parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
#             # use index to keep track of next variable
#             if (index + 1) < len(dataType):
#                 index += 1

        
    timeend = time.time()
    print 'Start time of pyGDP: ' + str(timestart)
    print 'End time of pyGDP: ' + str(timeend)
    print 'Total time of pyGDP: ' + str(timeend-timestart)
    
    os.chdir(dir)
#main_func(os.getcwd())