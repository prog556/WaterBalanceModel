def dataset_prop(data_set):
        if data_set == 'PRISM':
            ds_dict={'name':'PRISM', 'url':'http://cida.usgs.gov/thredds/dodsC/prism', 'timestep':'Monthly','Vars':['ppt','tmx','tmn']}
        return ds_dict

def get_GDP_data(zipfile,gageid,climate_dict,POR):
    myGDP = pyGDP.pyGDPwebProcessing()
    shapefiles = myGDP.uploadShapeFile(wkdir+'/'+zipfile)
##    shapefiles = myGDP.getShapefiles()
##    for shp in shapefiles:
##        print shp

    # feature loaded from sciencebase
    shapefile = 'upload:'+zipfile
    user_attribute = 'SiteId'
    user_value = None

    #The url of each dataset
    dataSet = climate_dict['url']

    #The precipitation and temperatures of each dataset. Start at position(not index) 5 until the end of the
    #dictionary's key(which is a list)
    dataType=climate_dict['Vars']

    #Start date
    timeBegin=POR['startTime']
    #End date
    timeEnd = POR['endTime']

    # data processing arguments
    gmlIDs=None
    verbose=True
    coverage = 'false'
    delim='COMMA'
    stats='MEAN'

    # run the pyGDP
    outputPath = myGDP.submitFeatureWeightedGridStatistics(shapefile, dataSet, dataType, timeBegin, timeEnd, user_attribute, user_value, gmlIDs, verbose, coverage, delim, stats)
    print outputPath
    # copy the output and rename it
    shutil.copy2(outputPath, climate_dict['name']+'_'+gageid+'.csv')

    # I combined the parse file to the end of the GDP module because it made
    # things simpler.  Check to make sure I didn't screw anything up.
    csvread = csv.reader(open(climate_dict['name']+'_'+gageid+'.csv', 'rb'))
    csvwrite = csv.writer(open(dataType[0]+'.csv', "wb"))

    index = 0

    temp = csvread
    var = temp.next()
    var[0] = '#'+dataType[0]
    gage = temp.next()

    csvwrite.writerow(var)
    csvwrite.writerow(gageid)
    parsedFiles = []
    for variable in dataType:

        for row in csvread:

            if variable == dataType[len(dataType) - 1]:
                csvwrite.writerow(row)
            else:
                if (row[0] in '#'+dataType[index+1]) or (row[0] in '# '+dataType[index+1]):
                    var = '#'+dataType[index+1]
                    csvwrite = csv.writer(open(dataType[index+1] + '.csv', "wb"))
                    row[1:] = ""
                    row[0] = var
                    csvwrite.writerow(row)
                    csvwrite.writerow(gage)

                    if len(dataType) == 2:
                        csvread.next()
                        csvwrite.writerow(csvread.next())
                    else:
                        csvread.next()
                        csvwrite.writerow(csvread.next())
                    break
                else:
                    if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
                        csvwrite.writerow(row)

        parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')
        print "Finished parsing " + variable + ".csv"
        if (index + 1) < len(dataType):
            index += 1

#**************************************************************
import sys
import os,pyGDP,shutil, csv, time
global wkdir

if __name__ == '__main__':
    #  set parameters
    gageid = '06746095'
    zipfile = 'G06746095_z'
    POR={'startTime':'2010-01-01T00:00:00.000Z','endTime':'2012-01-01T00:00:00.000Z'}
    data_set="PRISM"
    wkdir = 'D:/abock/temp'

    os.chdir(wkdir)
    climate_data = dataset_prop(data_set)
    get_GDP_data(zipfile,gageid,climate_data,POR)
