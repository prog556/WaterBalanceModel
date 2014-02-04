# dependencies OWSLIB, xmltree
import os,pyGDP,shutil, csv, time

global csvfile, vistrails_data_set, nhru, url

def main_func(curdir, set, region):
    
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
    
    def list_define(set):

        if set == 'cccma_cgmc3_1':
            return ['cccma_cgmc3'+str(scenario), 'http://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'cnrm_cm3':
            return ['cnrm_cm3'+str(scenario), 'http://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
             'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
             'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
             'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'gfdl_cm2_1':
            return ['gfdl_cm2_1'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'ipsl_cm4':
            return ['ipsl_cm4'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'miroc3_2_medres':
            return ['miroc3_2_medres'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'miub_echo_g':
            return ['miub_echo_g'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'mri_cgcm2_3_2a':
            return ['mri_cgcm2_3_2a'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
        elif set == 'mpi_echam5':
            return ['mpi_echam5'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
                 'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
                 'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
                 'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
     
    global csvfile, vt_dataset, nhru, length, vt_datatype, url
    import pyGDP
    
    Region_return=Region_lookup(region)
    hrus = Region_return[0]
    nhru = hrus
    ScienceBase_URL= Region_return[1]
     
    pyGDP.WFS_URL = ScienceBase_URL
    url = pyGDP.WFS_URL
    pyGDP = pyGDP.pyGDPwebProcessing()
     
    # change working directory so the GDP output will be written there
     
    # Datasets and their properties
    # run 1, 2 , and 3
     
    #**********************************
    # run 1 only
    #scenario = 'a2'
    # other scenarios are 'a1b' and 'b1'
    #scenarios = ['a2','a1b','b1']
    scenarios = ['a2', 'a1b']
     
    timestart = '2046-01-15T00:00:00.000Z'
    timeend='2100-12-15T00:00:00.000Z'
     
    #**********************************
    # Datasets for each scenario - note that mpi_echam5 is not run for scenario a1b
    #a1b
    #data=[cccma_cgmc3_1,cnrm_cm3,gfdl_cm2_1,ipsl_cm4,miroc3_2_medres,miub_echo_g,mri_cgcm2_3_2a]
    #a2
    #data=[cccma_cgmc3_1,cnrm_cm3,gfdl_cm2_1,ipsl_cm4,miroc3_2_medres,miub_echo_g,mpi_echam5,mri_cgcm2_3_2a]
    #b1
    #data=[cccma_cgmc3_1,cnrm_cm3,gfdl_cm2_1,ipsl_cm4,miroc3_2_medres,miub_echo_g,mpi_echam5,mri_cgcm2_3_2a]
     
    
    # get list of shapefiles uploaded to the GDP
    shapefiles = pyGDP.getShapefiles()
    for shp in shapefiles:
        print shp
     
    # feature loaded from sciencebase
    #should shapefile be sb:SP_hru instead?
    shapefile = 'sb:nhru'
    user_attribute = 'hru_id_loc'
     
    user_value = None
     
    os.chdir(curdir)
    dir = os.getcwd()
     
    vt_data = list_define(set)
    vt_datatype = vt_data[5:] 
    
    #for scenario in scenarios:  
         
#     cnrm_cm3 = ['cnrm_cm3'+str(scenario), 'http://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#          'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#          'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#          'cnrm_cm3-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     gfdl_cm2_1 = ['gfdl_cm2_1'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'gfdl_cm2_1-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     ipsl_cm4 = ['ipsl_cm4'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'ipsl_cm4-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     mpi_echam5 = ['mpi_echam5'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'mpi_echam5-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     miroc3_2_medres = ['miroc3_2_medres'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'miroc3_2_medres-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     cccma_cgmc3_1 = ['cccma_cgmc3'+str(scenario), 'http://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'cccma_cgcm3_1-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     miub_echo_g = ['miub_echo_g'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'miub_echo_g-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
#      
#     mri_cgcm2_3_2a = ['mri_cgcm2_3_2a'+str(scenario), 'dods://pcmdi8.llnl.gov/thredds/dodsC/bcca/BCCA_0.125deg-gregorian-sres-monthly', 'Monthly', timestart, timeend,\
#              'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-pr-BCCA_0-125deg-monthly',
#              'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-tasmax-BCCA_0-125deg-monthly',
#              'mri_cgcm2_3_2a-gregorian-sres'+str(scenario)+'-run1-tasmin-BCCA_0-125deg-monthly']
     
     
#         if scenario == 'a1b':
#             data=[cccma_cgmc3_1,cnrm_cm3,gfdl_cm2_1,ipsl_cm4,miroc3_2_medres,miub_echo_g,mri_cgcm2_3_2a]
#         elif scenario == 'a2':
#                 data=[cccma_cgmc3_1,cnrm_cm3,gfdl_cm2_1,ipsl_cm4,miroc3_2_medres,miub_echo_g,mpi_echam5,mri_cgcm2_3_2a]
    
    timestart = time.time()
    
    
    #################
    #scenarios = ['a2', 'a1b']
    scenario = 'a2'
    
    
    
    
    #for dataset in data:
    #file_loc = dir+'\\'+scenario+'\\'+dataset[0]
    file_loc = dir+'\\'+set
    if not os.path.exists(file_loc):
        os.mkdir(file_loc)
    os.chdir(file_loc)
    #print "The current scenario is: " +scenario + "dataset being worked on is: " + dataset[0]
    print "The current scenario is: " +scenario + "dataset being worked on is: " + set

    #The url of each dataset
    dataSet = vt_data[1]
    #dataSet = dataset[1]

    #The precipitation and temperatures of each dataset
    #Start at position(not index) 5 until the end of the
    #dictionary's key(which is a list)
      
    dataType=vt_data[5:]  
    #dataType = dataset[5:]
        
    # daily or monthly for additional aggregation/formatting (not appended yet)
    timeStep = vt_data[2]
    length = timeStep
    #timeStep = dataset[2]

    #Start date
    timeBegin = vt_data[3]
    #timeBegin = dataset[3]
    #End date
    timeEnd = vt_data[4]
    #timeEnd = dataset[4]

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
    
#     ind = 5
#     for var in range(5, len(dataset)):
#         line = dataset[var].split('-')
#         dataset[ind] = line[4]
#         ind += 1
#         
#     dataType = dataset[5:]
    
    #shutil.copy2(outputPath, region+'_'+dataset[0]+'.csv')
    shutil.copy2(outputPath, region+'_'+vt_data[0]+'.csv')
    
#     csvfile = os.getcwd()+region+'_'+dataset[0]+'.csv'       
#     #Parse the csv file 
#     index = 0            
#     
#     csvread = csv.reader(open(region+'_'+dataset[0] + '.csv', "rb")) 
#     
#     csvwrite = csv.writer(open(dataType[0] + '.csv', "wb"))
#         
#     temp = csvread
#     var = temp.next()
#     var[0] = '#'+dataType[0]
#     #Gets gage ids
#     gage = temp.next()
#     
#     #Writes current variable to csv file
#     csvwrite.writerow(var)
#     #Writes all gage ids to csv file
#     csvwrite.writerow(gage)
#     
#     for variable in dataType:                
#             
#         for row in csvread:
#             #if on last variable     
#             if variable == dataType[len(dataType) - 1]: 
#                 csvwrite.writerow(row)               
#             else:  
#                 if (row[0] in '#'+dataType[index+1]) or (row[0] in '# '+dataType[index+1]):
#                     #Line 33 is used for titling the csv file the name of the variable (like tmin, ppt, or tmax)
#                     var = '#'+dataType[index+1]
#                     parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
#                     csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
#                     row[1:] = ""
#                     row[0] = var
#                     csvwrite.writerow(row)
#                     csvwrite.writerow(gage)
#                     if len(dataType) == 2:
#                         csvread.next()
#                     else:
#                         csvread.next()
#                         csvwrite.writerow(csvread.next())
#                         csvwrite.writerow(csvread.next())
#                     break
#                 else:
#                     if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
#                         csvwrite.writerow(row)
#         print "Finished parsing " + variable + ".csv"
#         parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
#         # use index to keep track of next variable
#         if (index + 1) < len(dataType):
#             index += 1
        
    timeend = time.time()
    print 'Start time of pyGDP: ' + str(timestart)
    print 'End time of pyGDP: ' + str(timeend)
    print 'Total time of pyGDP: ' + str(timeend-timestart)
    

    os.chdir(dir)
