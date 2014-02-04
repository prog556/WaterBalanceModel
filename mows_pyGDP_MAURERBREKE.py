# dependencies OWSLIB, xmltree
import os,shutil, csv, time

def main_func(region, currdir, timestart, timeend):#, scenarios):
    
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
            
    
    global parsedFiles, csvfile, vistrails_data_set, nhru, url
    import pyGDP
    #region = 'R13'
    parsedFiles = []
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
    
    #ends 2012
    timestart = '1950-01-15T00:00:00.000Z'
    timeend='1960-12-15T00:00:00.000Z'
    
    shapefiles = pyGDP.getShapefiles()
    for shp in shapefiles:
        print shp
    
    shapefile = 'sb:nhru'
    user_attribute = 'hru_id_loc'
    
    user_value = None
    
    #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\MAURERBREKE')
    dir = currdir
    
    gcmRun = '1'
    for scenario in scenarios:
        cccma_cgcm3_1_1 = ['sres'+scenario+'_cccma-cgcm3-1_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                           'sres'+scenario+'_cccma-cgcm3-1_1_Prcp',
                           'sres'+scenario+'_cccma-cgcm3-1_1_Tavg']
        gfdl_cm2_1_1_1 = ['sres'+scenario+'_gfdl-cm2-1_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                          'sres'+scenario+'_gfdl-cm2-1_1_Prcp',
                          'sres'+scenario+'_gfdl-cm2-1_1_Tavg']
        miroc3_2_medres_1 = ['sres'+scenario+'_miroc3-2-medres_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                             'sres'+scenario+'_miroc3-2-medres_1_Prcp',
                             'sres'+scenario+'_miroc3-2-medres_1_Tavg']
        miub_echo_g_1_1 = ['sres'+scenario+'_miub-echo-g_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                           'sres'+scenario+'_miub-echo-g_1_Prcp',
                           'sres'+scenario+'_miub-echo-g_1_Tavg']
        mpi_echam5_1 = ['sres'+scenario+'_mpi-echam5_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                        'sres'+scenario+'_mpi-echam5_1_Prcp',
                        'sres'+scenario+'_mpi-echam5_1_Tavg']
        mri_cgcm2_3_2a_1 = ['sres'+scenario+'_mri-cgcm2-3-2a_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_mri-cgcm2-3-2a_1_Prcp',
                            'sres'+scenario+'_mri-cgcm2-3-2a_1_Tavg']
        # New MaurerBreke Statistically downscaled datasets (put with other MB datasets)
        bccr_bcm2_0 = ['sres'+scenario+'_bccr-bcm2-0_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                           'sres'+scenario+'_bccr-bcm2-0_'+gcmRun+'_Prcp',
                           'sres'+scenario+'_bccr-bcm2-0_'+gcmRun+'_Tavg']
        cnrm_cm3 = ['sres'+scenario+'_cnrm-cm3_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_cnrm-cm3_'+gcmRun+'_Prcp',
                            'sres'+scenario+'_cnrm-cm3_'+gcmRun+'_Tavg']
        csiro_mk3_0 = ['sres'+scenario+'_csiro-mk3-0_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_csiro-mk3-0_'+gcmRun+'_Prcp',
                            'sres'+scenario+'_csiro-mk3-0_'+gcmRun+'_Tavg']
        giss_model_e_r = ['sres'+scenario+'_giss-model-e-r_2','dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                           'sres'+scenario+'_giss-model-e-r_2_Prcp',
                           'sres'+scenario+'_giss-model-e-r_2_Tavg']
        inmcm3_0 = ['sres'+scenario+'_inmcm3-0_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                          'sres'+scenario+'_inmcm3-0_'+gcmRun+'_Prcp',
                          'sres'+scenario+'_inmcm3-0_'+gcmRun+'_Tavg']
        ipsl_cm4 = ['sres'+scenario+'_ipsl-cm4_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                          'sres'+scenario+'_ipsl-cm4_'+gcmRun+'_Prcp',
                          'sres'+scenario+'_ipsl-cm4_'+gcmRun+'_Tavg']
        ncar_ccsm3_0 = ['sres'+scenario+'_ncar-ccsm3-0_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_ncar-ccsm3-0_'+gcmRun+'_Prcp',
                            'sres'+scenario+'_ncar-ccsm3-0_'+gcmRun+'_Tavg']
        ncar_pcm1 = ['sres'+scenario+'_ncar-pcm1_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_ncar-pcm1_'+gcmRun+'_Prcp',
                            'sres'+scenario+'_ncar-pcm1_'+gcmRun+'_Tavg']
        ukmo_hadcm3 = ['sres'+scenario+'_ukmo-hadcm3_'+gcmRun,'dods://cida.usgs.gov/thredds/dodsC/maurer/maurer_brekke_w_meta.ncml','Monthly',timestart,timeend,\
                            'sres'+scenario+'_ukmo-hadcm3_'+gcmRun+'_Prcp',
                            'sres'+scenario+'_ukmo-hadcm3_'+gcmRun+'_Tavg']
    
        data = [cccma_cgcm3_1_1,gfdl_cm2_1_1_1,miroc3_2_medres_1,miub_echo_g_1_1,mpi_echam5_1,mri_cgcm2_3_2a_1]
    
        for dataset in data:
            if len(scenario) == 2:
                name = dataset[0]
                name = name[7:]
            else:
                name = dataset[0]
                name = name[8:]
            file_loc = str(dir.name)+'\\Step1_CLIMATE_DATA\\'+region+'\\'+scenario+'\\'+name
            if not os.path.exists(file_loc):
                os.mkdir(file_loc)
            os.chdir(file_loc)
            print "The current dataset being worked on is: " + name
    
            dataSet = dataset[1]
    
            dataType = dataset[5:]
    
            timestep = dataset[2]
    
            timeBegin = dataset[3]
            timeEnd = dataset[4]
    
            gmlIDs = None
            verbose = True
    
            coverage = Region_return[2]
            delim = 'COMMA'
            stats = 'MEAN'
    
            start = time.time()
            outputPath = pyGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
            end = time.time()
            
            print "Start time is: " + str(start)
            print 'End time is: ' + str(end)
            print 'Total time was: ' + str(end-start)
            print outputPath
    
            shutil.copy2(outputPath, region+'_'+name+'.csv')
            
            csvfile = os.getcwd()+region+'_'+name+'.csv'

#             dataType = ['Prcp', 'Tavg']
#             vistrails_data_set = ['Prcp', 'Tavg']
            
            #csvread = csv.reader(open(region+'_'+name+'.csv', 'rb'))
            
            #csvwrite = csv.writer(open(dataType[0]+'.csv', 'wb'))
            #parsedFiles.append(dataType[0]+'.csv')
            #index = 0
    
            #temp = csvread
            #var = temp.next()
            #var[0] = '#'+dataType[0]
    
            #gage = temp.next()
    
            #csvwrite.writerow(var)
            #csvwrite.writerow(gage)
    
#             for variable in dataType:
#     
#                 for row in csvread:
#                     if variable == dataType[len(dataType) - 1]:
#                         csvwrite.writerow(row)
#                     else:
#                         if (row[0] in '#'+dataType[index+1]) or (row[0] in '# ' + dataType[index+1]):
#                             var = '#'+dataType[index+1]
#                             csvwrite = csv.writer(open(dataType[index+1] + '.csv', 'wb'))
#                             parsedFiles.append(dataType[index+1]+'.csv')
#                             row[1:] = ''
#                             row[0] = var
#                             csvwrite.writerow(row)
#                             csvwrite.writerow(gage)
#     
#                             if len(dataType) == 2:
#                                 csvwrite.writerow(csvread.next())
#                             else:
#                                 csvread.next()
#                                 csvwrite.writerow(csvread.next())
#                                 csvwrite.writerow(csvread.next())
#                             break
#                         else:
#                             if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
#                                 csvwrite.writerow(row)
#                 print 'Finished parsing ' + variable + '.csv'
#     
#                 if (index+1)<len(dataType):
#                     index += 1
#     
#                 os.chdir(dir)
    
    
#main_func('nhru', os.getcwd(), '', '')