import os, time, numpy

from calendar import monthrange
# Call function
# three arguments
#   1-numpy module
#   2-Tile
#   3-climate datasset
#   4 - number of hrus

# changes from PPt.csv to PPT_month.txt
# 1 - strip off header (top 3 lines)
# 2 - reformat the date to year month
# 3 - convert units (mm to inches, deg C to deg F)
# 4 - go from comma-delimited to white-space delimited

#Andy ideas to make faster
#1 - strip off header,strip off first column date - left with dataframe (rows - # of months, columns - # of hrus)
#2 - with stripped off dates, sepearate year and month into lists as floats, get count
#2 - create numpy matrix of dimensions (months - rows, number of hrus +2 (1 column for year, 1 column for month) - columns)
#3 - Read data into matrix as a whole
#4 - populate column 1 (position 0) with year, populate column 2 (position 1) with month
#5 - write out matrix as textfile:
#  numpy.savetxt('params.txt'(directory to be saved into), params(name of matrix), fmt='%1.5f', delimiter='  ')
# arguments for savetxt 0 - filename, 1 - matrix name, 2- datatype (float in this case), 3 - delimiter/separater)
# look through 


global WBM_Files, PORFile

WBM_Files = []

def add_row_temp(var, current_var_float, newline):
    #var_units = [x*0.0393 for x in current_var_float]
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' '+ str1
    newline_float = map(float, newline.split())
    return newline_float

def add_row_pr(var, current_var_float, newline):
    #var_units = [x*0.0393 for x in current_var_float]
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' '+ str1
    newline_float = map(float, newline.split())
    return newline_float

def Format_monthly(region,tile,dataset,nhru, WFS_URL, curdir):
    # begin time
    timeStart = time.time()
    osTimes1 = os.times()
    
    os.chdir(curdir+'\\'+dataset)
    
    thisdir = os.getcwd()#+'\\Step1_CLIMATE_DATA\\'+region+'\\SBDDS\\'+dataset
    #thisdir = os.getcwd()+'\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_CC\\'+dataset
    #thisdir = os.getcwd()+'\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_FC\\a2\\'+dataset
    #thisdir = os.getcwd()+'\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_FC\\a1b\\'+dataset
    #thisdir = os.getcwd()+'\\Step1_CLIMATE_DATA\\'+region+'\\MAURERBREKE\\a2\\'+dataset
    #thisdir = os.getcwd()+'\\Step1_CLIMATE_DATA\\'+region+'\\MAURERBREKE\\a1b\\'+dataset
      
    #SBDDS
    if dataset == 'PRISM':
        varlist=["ppt","tmx", "tmn"] 
    elif dataset == 'GENMON' or dataset == 'MPI ECHAM5' or dataset == 'NOAA NCEP' or dataset == 'GFDL CM 2.0':
        varlist = ["RT", "TA"]
    else:
        varlist = ['pr', 'tasmax', 'tasmin']      
       
    #varlist = ['Prcp', 'Tavg']  
    #varlist = ['RT', 'TA']  
    years_list = []
    months_list = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12]

   

    for var in varlist:
        inputfile = open(thisdir+'\\'+var+'.csv', 'r')
        filelines = inputfile.readlines()
        matrix_row = 0
        if var in varlist[0]:
            PORfile = open(thisdir+'\\POR.txt','w')
        #len(filelines[3:]) is number of rows and nhru is number of columns
        matrix = numpy.zeros(shape = (len(filelines[3:]), nhru+2))
        
        head = 'Dataset = ' + dataset + \
        '\nVariable = ' + var + \
        '\nRegion = ' + region + \
        '\nhru = ' + str(nhru) + \
        '\n' + WFS_URL

        for line in filelines[3:]: 
            
            #First section is getting the month and the date
            splitline = line.split(',')
            timestamp = splitline[0].split('T')
            yrmoday = timestamp[0].split('-')
            #Year and month are both strings
            year = yrmoday[0]
            month = yrmoday[1]
            newline = year + ' ' + month
            print 'Year: ' + year + ' Month: ' + month
            #newline = year+' '+str(month)+' '
            
            #print newline
            #current_var_str = splitline[1:]
            current_var_float = [float(x) for x in splitline[1:]]
            
            if var == 'ppt' or var == 'RT' or var == 'pr' or var == 'Prcp':
                matrix[matrix_row,...] = add_row_pr(var, current_var_float, newline)
                PORfile.writelines(str(year)+'-'+str(month)+'-01 \n')
                if int(year) not in years_list:
                    years_list.append(int(year))
            elif var == 'tmin' or var == 'tmax' or var == 'tmn' or var == 'tmx' or var == 'TA' or var == 'tasmin' or var == 'tasmax' or var == 'Tavg':
                matrix[matrix_row,...] = add_row_temp(var, current_var_float, newline)
            else:
                print "You shouldn't enter this else statement"
                
            #if var in varlist[0]:         
                #PORfile.writelines(str(year)+'-'+str(month)+'-01 \n')
            if matrix_row == 0:
                start_date = str(month) + '-' + str(year)
                head += '\nmonthly ' + start_date + ' - '
            matrix_row += 1
#       for i in range(1,len(splitline)):
#                 #if dataset == 'PRISM':
#                 if var != 'ppt':
#                     newline += str((float(splitline[i].rstrip())*1.8)+32)+' ' # Celsius to Fahrenheit
#                 if var == 'ppt':
#                     newline = newline +str(float(splitline[i].rstrip())*.0393)+' '# mm to inches
#             if var == 'ppt':
#                 PORline = str(year)+'-'+str(month)+'-01 \n'
#                 PORfile.writelines(PORline)
#                 PORcount += 1
            #newline += '\n'
        end_date = str(month) + '-' + str(year)
        end_year = int(year)
        head += end_date + '\n######'
        
        if var == 'ppt' or var == 'RT' or var == 'pr' or var =='Prcp':
            
            if dataset != 'PRISM':
                nodays = []
               
                for i in years_list:
                    for j in months_list:
                        #print monthrange(i, j)
                        days = str(monthrange(i,j)[1])
                        if i == end_year and j == 12:
                            #nodays.append(float(days))
                            break
                        else:
                            nodays.append(float(days))

                
                conversion = numpy.array(nodays)
                row = 0
                print len(conversion)
                print len(filelines[3:])
                for x in conversion:
                    #matrix[row,0:2] = matrix[row,0:2]
                    matrix[row,2:] = x*matrix[row,2:]
                    row += 1
            var = 'PPT'        
            numpy.savetxt(thisdir + '\\'+var+'_month.txt', matrix, '%1.5f', ' ', header = head)
            WBM_Files.append(thisdir+'\\PPT_month.txt')
            PORFile = thisdir+'\\POR.txt'
        elif var == 'tmin' or var == 'tmn' or var == 'tasmin':
            tmin = matrix
            numpy.savetxt(thisdir+'\\'+var+'_month.txt', matrix, '%1.5f', ' ', header = head)
            WBM_Files.append(thisdir+'\\'+var+'_month.txt')
        elif var == 'tmax' or var == 'tmx' or var == 'tasmax':
            tmax = matrix
            numpy.savetxt(thisdir+'\\'+var+'_month.txt', matrix, '%1.5f', ' ', header = head)
            WBM_Files.append(thisdir+'\\'+var+'_month.txt')
        elif var == 'TA' or var == 'Tavg':
            var = 'TAVE'
            numpy.savetxt(thisdir+'\\'+var+'_month.txt', matrix, '%1.5f', ' ', header = head)
            WBM_Files.append(thisdir+'\\'+var+'_month.txt')
        inputfile.close()
        print var+'.txt is finished formatting'
        PORFile = thisdir+'\\POR.txt'
        PORfile.close()

    if 'TA' not in varlist and 'Tavg' not in varlist:
        tave = numpy.add(tmin, tmax)/2
        head = 'Dataset = ' + dataset + \
        '\nVariable = tave' \
        '\nRegion = ' + str(region) + \
        '\nhru = ' + str(nhru) + \
        '\n' + WFS_URL + \
        '\ndaily ' + start_date + ' - ' + end_date + \
        '\n######'
        numpy.savetxt(thisdir+'\\TAVE_month.txt', tave, '%1.5f', ' ', header = head)
        print "TAVE.txt is finished formatting"

    timeEnd = time.time()
    osTimes2 = os.times()
    utime = osTimes2[0] - osTimes1[0]
    stime = osTimes2[1] - osTimes1[1]

    print "Clock time was %s seconds" % (timeEnd - timeStart)
    print "utime = %s, stime = %s" % (utime, stime)

  


    
    
#old, extra loops 
#     #*********************************************************************
#     # write and format final temp file
#     tmaxfile = thisdir+'\\tmax_month.txt'
#     tminfile = thisdir+'\\tmin_month.txt'
#     #add  tmax and tmin files to vistrails here
# #   Step1.setTmin(tminfile)
# #   Step1.setTmax(tmaxfile)
#     
#     tavefile = 'TAVE_month.txt'
#     outputfile = open (thisdir+'\\'+tavefile, 'a')
#     files = [tmaxfile,tminfile]
# 
#     #PORcount is number of columns and nhru is number of rows
#     tmax = numpy.zeros(shape = (PORcount,nhru))
#     tmin = numpy.zeros(shape = (PORcount,nhru))
# 
#     #empty list of dateList
#     dateList=[]
#     #loop through len(files) with variable i
#     for i in range (0,len(files)):
#         count = 0
#         #files[i] is tmaxfile or tminfile
#         infile = open(files[i], 'r')
#         #filelines contains all lines in files[i]
#         filelines = infile.readlines()
#         #loop through the rows of filelines
#         for lines in filelines[0:tmax.shape[0]]:
#             #items is a list delimited by a whitespace
#             items = lines.split(' ')
#             #if on first variable(tmax), 
#             if i == 0:
#                 #at the row of count adds index two(or the first temp) to the end to tmax
#                 tmax[count,...]=items[2:]
#             #if on second variable(tmin)
#             if i == 1:
#                 #at the row of count adds index two(or the first temp) to the end to tmin
#                 tmin[count,...]=items[2:]
#             #newstring is the year and month in that order
#             newstring = items[0]+' '+items[1]+' '
#             #add newstring to the end of datelist
#             dateList.append(newstring)
#             count += 1
#     infile.close()
# 
#     #tave is an array of the average of tmax and tmin
#     tave = numpy.add(tmax,tmin)/2
#     #tave = temp_sum/2
# 
#     #loop through the rows of tave
#     for i in range(0,tave.shape[0]):
#         #newstring is year and month for each row
#         newstring = dateList[i]
#         #loop through 
#         for j in range(0,tave.shape[1]):
#             newstring = newstring+str(tave[i][j])+' '
#         newstring = newstring+'\n'
#         outputfile.writelines(newstring)
#     print 'done converting files for use in WBM'
#     #add tave file to vistrails here
#     #Step1.setTave(outputfile)
#     
#     outputfile.close()




