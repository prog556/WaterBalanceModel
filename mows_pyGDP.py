# dependencies OWSLIB, xmltree
import os,pyGDP,shutil, csv

global parsedFiles, csvfile, region


def main_func(region):
    #NHDplus region
    region = 'R06'
    #region = pyGDP.getRegion()
    # change working directory so the GDP output will be written there
        
    # Datasets and their properties
    #**********************************
    Gridded_Observed_Data_1950_1999 = ['Gridded Observed Data(1950-1999)', 'dods://cida.usgs.gov/thredds/dodsC/gmo/GMO_w_meta.ncml', 'Daily', '1950-01-01T00:00:00.000Z', '1999-12-31T00:00:00.000Z', 'Prcp', 'Tavg']
    Gridded_Observed_Data_1949_2010 = ['Gridded Observed Data(1949-2010)', 'http://cida.usgs.gov/thredds/dodsC/new_gmo', 'Daily', '1950-01-01T00:00:00.000Z', '1950-02-01T00:00:00.000Z', 'pr', 'tas']
    PRISM = ['PRISM', 'http://cida.usgs.gov/thredds/dodsC/prism', 'Monthly', '1895-01-01T00:00:00.000Z', '2012-12-31T00:00:00.000Z', 'ppt', 'tmx', 'tmn']
    DAYMET = ['DAYMET', 'dods://cida-eros-mows1.er.usgs.gov:8080/thredds/dodsC/daymet', 'Daily', '1980-01-01T00:00:00.000Z', '2012-01-01T00:00:00.000Z', 'prcp', 'tmax', 'tmin']
    MPI_ECHAM5 = ['MPI ECHAM5', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/EH5/merged/Monthly/RegCM3_Monthly_merged_EH5.ncml', 'Monthly', '1968-01-01T00:00:00.000Z', '2099-12-31T00:00:00.000Z', 'RT', 'TA']
    GENMON = ['GENMON', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GENMOM/merged/Monthly/RegCM3_Monthly_merged_GENMOM.ncml', 'Monthly', '1980-01-01T00:00:00.000Z', '2089-12-31T00:00:00.000Z', 'RT', 'TA']
    GFDL_CM_2_0 = ['GFDL CM 2.0', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/GFDL/merged/Monthly/RegCM3_Monthly_merged_GFDL.ncml', 'Monthly', '1980-01-01T00:00:00.000Z', '2069-12-31T00:00:00.000Z', 'RT', 'TA']
    NOAA_NCEP = ['NOAA NCEP', 'http://regclim.coas.oregonstate.edu:8080/thredds/dodsC/regcmdata/NCEP/merged/Monthly/RegCM3_Monthly_merged_NCEP.ncml','Monthly', '1982-01-01T00:00:00.000Z', '2007-12-31T00:00:00.000Z','RT','TA']
    
    #List dataset names
    data = [Gridded_Observed_Data_1950_1999, Gridded_Observed_Data_1949_2010,PRISM,DAYMET,MPI_ECHAM5,GENMON,GFDL_CM_2_0,NOAA_NCEP]
    #data=[Gridded_Observed_Data_1950_1999]
    
    # link to region 6 hrus on ScienceBase
    # put a function here to retrieve sciencebase url and number of hrus for specific region
    pyGDP.WFS_URL = 'https://www.sciencebase.gov/catalogMaps/mapping/ows/51b0d374e4b030b519830d73'
    
    #Get pyGDP.WFS_URL from vistrials
    #pyGDP.WFS_URL = pyGDP.get_pyGDP_WFS_URL()
    
    # region 6 = 2303 hrus
    # for more info read:
    # science base access:  https://my.usgs.gov/confluence/display/GeoDataPortal/pyGDP+FAQ
    
    # call web processing module
    # will automatically use shapefiles from GDP as default unless
    # you define web service
    pyGDP = pyGDP.pyGDPwebProcessing()
    
    # get list of shapefiles uploaded to the GDP
    shapefiles = pyGDP.getShapefiles()
    for shp in shapefiles:
        print shp
    
    # feature loaded from sciencebase
    # automate region number
    shapefile = 'sb:R06a_hru'
    
    # shapefile/feature attribute for which you are summarizing info
    user_attribute = 'hru_id_loc'
    
    # create list of hru_ids that can be used for the uservalue
    # need to automate number of hurs in shapefile, maybe include from scienecbase
    # url retrieval above lin 25-29
   
    
    # single feature id test case
    #user_value = '10'
    # to summarize for all ids
    user_value = None
    
    for dataset in data:
        print "The current dataset being worked on is: " + dataset[0]
    
        #The url of each dataset
        dataSet = dataset[1]
    
        #The precipitation and temperatures of each dataset
        #Start at position(not index) 5 until the end of the
        #dictionary's key(which is a list)
        dataType=dataset[5:]
    
        # daily or monthly for additional aggregation/formatting (not appended yet)
        timeStep = dataset[2]
    
        #Start date
        timeBegin = dataset[3]
        #End date
        timeEnd = dataset[4]
    
        # data processing arguments
        gmlIDs=None
        verbose=True
        #coverage = 'false' check if on US border/ocean
        coverage='true'
        delim='COMMA'
        stats='MEAN'
    
        # run the pyGDP
        outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
        print outputPath
        #pyGDP.setCSV_file(outputPath)
        # copy the output and rename it
        shutil.copy2(outputPath, region+'_'+dataset[0]+'.csv')
        
        csvfile = os.getcwd()+region+'_'+dataset[0]+'.csv'
        
        #Parse the csv file 
        index = 0
        #parsedFiles = []
            
        csvread = csv.reader(open(outputPath + '.csv', "rb")) 
        csvwrite = csv.writer(open(dataType[0] + '.csv', "wb"))
        
        
        temp = csvread
        var = temp.next()
        #Gets gage ids
        gage = temp.next()
        
        #Writes current variable to csv file
        csvwrite.writerow(var)
        #Writes all gage ids to csv file
        csvwrite.writerow(gage)
        
        for variable in dataType:                
                
            for row in csvread:
                #if on last variable     
                if variable == dataType[len(dataType) - 1]: 
                    csvwrite.writerow(row)               
                else:  
                    if (row[0] in '#'+dataType[index+1]) or (row[0] in '# '+dataType[index+1]):
                        #Line 33 is used for titling the csv file the name of the variable (like tmin, ppt, or tmax)
                        var = '#'+dataType[index+1]
                        parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
                        csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                        row[1:] = ""
                        row[0] = var
                        csvwrite.writerow(row)
                        csvwrite.writerow(gage)
                        if len(dataType) == 2:
                            csvread.next()
                        else:
                            temp = csvread
                            csvwrite.writerow(csvread.next())
                            csvwrite.writerow(temp.next())
                        break
                    else:
                        if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
                            csvwrite.writerow(row)
            print "Finished parsing " + variable + ".csv"
            parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
            # use index to keep track of next variable
            if (index + 1) < len(dataType):
                index += 1
                
