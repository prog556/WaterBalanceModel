# dependencies OWSLIB, xmltree
import os,pyGDP,shutil, csv, time

def main_func():
    
    def Region_lookup(region):
        region_properties = []
        if region == 'nhru':
            region_properties.append(371)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d35da1e4b0ca184833940c')
            region_properties.append('false')
        if region == 'R01':
            region_properties.append(2462)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5244735ae4b05b217bada04e')
            region_properties.append('false')
        if region == 'R02':
            region_properties.append(4827)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52696784e4b0584cbe9168ee')
            region_properties.append('false')
        if region == 'R03':
            region_properties.append(9899)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5283bd23e4b047efbbb57922')
            region_properties.append('false')
        if region == 'R04':
            region_properties.append(5936)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/5284ff57e4b063f258e61b9d')
            region_properties.append('false')
        if region == 'R05':
            region_properties.append(7182)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/528516bbe4b063f258e62161')
            region_properties.append('false')
        if region == 'R06':
            region_properties.append(2303)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/51d75296e4b055e0afd5be2c')
            region_properties.append('true')
        if region == 'R07':
            region_properties.append(8205)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52851cd5e4b063f258e643dd')
            region_properties.append('true')
        if region == 'R08':
            region_properties.append(4449)
            region_properties.append('https://www.sciencebase.gov/catalogMaps/mapping/ows/52854695e4b063f258e6513c')
            region_properties.append('true')
        if region == 'R10L':
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
    
    global parsedFiles, csvfile, vistrails_data_set, nhru, length
    
    regions = ['R06', 'R10L', 'R11', 'R12', 'R13', 'R14']
    region = 'R06'
    parsedFiles = []
    csvfile = ''
    vistrails_data_set = []
    
    Region_return=Region_lookup(region)
    hrus = Region_return[0]
    nhru = hrus
    ScienceBase_URL= Region_return[1]
    
    pyGDP.WFS_URL = ScienceBase_URL
    
    # call web processing module
    
    pyGDP = pyGDP.pyGDPwebProcessing()
    
    # change working directory so the GDP output will be written there
    
    # Datasets and their properties
    # run 1, 2 , and 3
    
    #**********************************
    # run 1 only
    #scenario = 'a2'
    # other scenarios are 'a1b' and 'b1'
    scenarios = ['a2','a1b'] # not running b1 or a1fi
    
    timestart = '1960-01-15T00:00:00.000Z'
    timeend = '2010-12-15T00:00:00.000Z'
    
    #     timestart = '2010-12-15T00:00:00.000Z'
    #     timeend='2099-12-15T00:00:00.000Z'
    
    #**********************************
    # datasets greyed out - we are not initially using.
    ##ccsm = ['ccsm'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
    ##    'ccsm-'+scenarios[0]+'-pr-NAm-grid',
    ##    'ccsm-'+scenarios[0]+'-tmax-NAm-grid',
    ##    'ccsm-'+scenarios[0]+'-tmin-NAm-grid']
    
    
    
    
    shapefiles = pyGDP.getShapefiles()
    for shp in shapefiles:
        print shp
    
    # feature loaded from sciencebase
    #should shapefile be sb:SP_hru instead?
    shapefile = 'sb:'+region+'_hru'
    user_attribute = 'hru_id_loc'
    
    user_value = None
    
    os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\HAYHOE')
    dir = os.getcwd()
    
    for scenario in scenarios:
    
        cgcm3_t47 = ['cgcm3_t47'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'cgcm3_t47-'+str(scenario)+'-pr-NAm-grid',
                'cgcm3_t47-'+str(scenario)+'-tmax-NAm-grid',
                'cgcm3_t47-'+str(scenario)+'-tmin-NAm-grid']
        
        cgcm3_t63 = ['cgcm3_t63'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'cgcm3_t63-'+str(scenario)+'-pr-NAm-grid',
                'cgcm3_t63-'+str(scenario)+'-tmax-NAm-grid',
                'cgcm3_t63-'+str(scenario)+'-tmin-NAm-grid']
        
        cnrm = ['cnrm'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'cnrm-'+str(scenario)+'-pr-NAm-grid',
                'cnrm-'+str(scenario)+'-tmax-NAm-grid',
                'cnrm-'+str(scenario)+'-tmin-NAm-grid']
        
        ##csiro = ['csiro'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'csiro-'+scenarios[0]+'-pr-NAm-grid',
        ##        'csiro-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'csiro-'+scenarios[0]+'-tmin-NAm-grid']
        
        ##echam5 = ['echam5'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'echam5-'+scenarios[0]+'-pr-NAm-grid',
        ##        'echam5-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'echam5-'+scenarios[0]+'-tmin-NAm-grid']
        
        echo = ['echo'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'echo-'+str(scenario)+'-pr-NAm-grid',
                'echo-'+str(scenario)+'-tmax-NAm-grid',
                'echo-'+str(scenario)+'-tmin-NAm-grid']
        
        gfdl_2_1 = ['gfdl_2-1'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'gfdl_2-1-'+str(scenario)+'-pr-NAm-grid',
                'gfdl_2-1-'+str(scenario)+'-tmax-NAm-grid',
                'gfdl_2-1-'+str(scenario)+'-tmin-NAm-grid']
        
        ##giss_aom = ['giss_aom'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'giss_aom-'+scenarios[0]+'-pr-NAm-grid',
        ##        'giss_aom-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'giss_aom-'+scenarios[0]+'-tmin-NAm-grid']
        
        ##hadcm3 = ['hadcm3'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'hadcm3-'+scenarios[0]+'-pr-NAm-grid',
        ##        'hadcm3-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'hadcm3-'+scenarios[0]+'-tmin-NAm-grid']
        
        ##miroc_hi = ['miroc_hi'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'miroc_hi-'+scenarios[0]+'-pr-NAm-grid',
        ##        'miroc_hi-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'miroc_hi-'+scenarios[0]+'-tmin-NAm-grid']
        
        miroc_med = ['miroc_med'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'miroc_med-'+str(scenario)+'-pr-NAm-grid',
                'miroc_med-'+str(scenario)+'-tmax-NAm-grid',
                'miroc_med-'+str(scenario)+'-tmin-NAm-grid']
        
        mri_cgcm2 = ['mri_cgcm2'+str(scenario), 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
                'mri_cgcm2-'+str(scenario)+'-pr-NAm-grid',
                'mri_cgcm2-'+str(scenario)+'-tmax-NAm-grid',
                'mri_cgcm2-'+str(scenario)+'-tmin-NAm-grid']
        
        ##pcm = ['pcm'+scenarios[0], 'http://cida.usgs.gov/thredds/dodsC/dcp/conus', 'Daily', timestart, timeend,\
        ##        'pcm-'+scenarios[0]+'-pr-NAm-grid',
        ##        'pcm-'+scenarios[0]+'-tmax-NAm-grid',
        ##        'pcm-'+scenarios[0]+'-tmin-NAm-grid']
        # get list of shapefiles uploaded to the GDP
    
    
    
        if scenario == 'a1b':
            #data=[cgcm3_t47,cgcm3_t63,cnrm,echam5,echo,giss_aom,hadcm3,miroc_hi,pcm]
            data=[cgcm3_t47,cgcm3_t63,cnrm,echo]
        elif scenario == 'a2':
            #data=[ccsm,cgcm3_t47,cgcm3_t63,cnrm,csiro,echam5,echo,gfdl_2_1,hadcm3,miroc_med,mri_cgcm2,pcm]
            data = [cgcm3_t47,cgcm3_t63,cnrm,echo,gfdl_2_1,miroc_med,mri_cgcm2]
    
        for dataset in data:
            file_loc = dir+'\\'+scenario+'\\'+dataset[0]
            if not os.path.exists(file_loc):
                os.mkdir(file_loc)
            os.chdir(file_loc)
            print "The current dataset being worked on is: " + dataset[0]
    
    
            #The url of each dataset
            dataSet = dataset[1]
    
            #The precipitation and temperatures of each dataset
            #Start at position(not index) 5 until the end of the
            #dictionary's key(which is a list)
    
            dataType = dataset[5:]
    
            # http://cida.usgs.gov/thredds/dodsC/dcp/conus or Daily for additional aggregation/formatting (not appended yet)
            timeStep = dataset[2]
    
            #Start date
            timeBegin = dataset[3]
            #End date
            timeEnd = dataset[4]
    
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
            shutil.copy2(outputPath, region+'_'+dataset[0]+'.csv')
    
            ind = 5
            for var in range(5, len(dataset)):
                line = dataset[var].split('-')
                dataset[ind] = line[2]
                ind += 1
    
            dataType = dataset[5:]
    
            #Parse the csv file
            index = 0
            #parsedFiles = []
    
    
            csvread = csv.reader(open(region+'_'+dataset[0] + '.csv', "rb"))
    
            csvwrite = csv.writer(open(dataType[0] + '.csv', "wb"))
            #parsedFiles.append(csvwrite)
    
            temp = csvread
            var = temp.next()
            var[0] = '#'+dataType[0]
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
                            csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                            #parsedFiles.append(csvwrite)
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
                # use index to keep track of next variable
                if (index + 1) < len(dataType):
                    index += 1
                #pyGDP.setCSV_Parsed_Files(parsedFiles)
            os.chdir(dir)
            
