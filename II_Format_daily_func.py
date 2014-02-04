import os, time, numpy
from calendar import monthrange

# Call function
# three arguments
#   1-numpy module
#   2-Tile
#   3-climate datasset
#   4 - number of hrus

# how to improve the speed
    # 1 - create numpy matrix (# of rows = # of days,
            # of cols = # hrus +3,column[0] = year, column[1]=month, column[2]=day
    # 2 - convert/calculate each row, add to matrix (in a loop)
    # 3 - write out textfile with numpy.writetxt (allows control for formatting i.e.
    #       decimal places, headers, etc.
    # 4 - numpy.savetxt(thisdir+'\gage_params_raw.txt', hru_final, fmt='%1.5f', delimiter='  ')
    #   0 - name/location of file you are writing, 1 - name of numpy matrix, 2 - format, 3 - delimiter
# extra - read data from text right into numpy matrix
    # data2 = numpy.genfromtxt(inputfile, dtype=None,delimiter=",",skip_header=3,usecols = range(1,2000))

global WBM_Files, PORFile
WBM_Files = []

def add_row_temp(var, current_var_float, newline):
    # var_units = [x*0.0393 for x in current_var_float]
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' ' + str1
    newline_float = map(float, newline.split())
    return newline_float

def add_row_pr(var, current_var_float, newline):
    # var_units = [x*0.0393 for x in current_var_float]
    str1 = ' '.join(str(x) for x in current_var_float)
    newline += ' ' + str1
    newline_float = map(float, newline.split())
    return newline_float

def Format_daily(region, tile, dataset, nhru, WFS_URL, curdir):  # , csvs, data, thisdir):
    # begin time
    timeStart = time.time()
    osTimes1 = os.times()
    
    
    os.chdir(curdir)
    thisdir = os.getcwd() + '\\' + dataset
   
    # thisdir = os.getcwd()+'\\'+dataset+'\\'+region+"\\"+region+tile 
  
    # varlist=["pr", "tas"]
    if dataset == 'DAYMET':
        varlist = ['prcp', 'tmax', 'tmin']
    else:
        varlist = ['pr', 'tas']
        
    years_list = []
    months_list = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12]
   
    for var in varlist:
        inputfile = open(thisdir + '\\' + var + '.csv', 'r')
        filelines = inputfile.readlines()
        matrix_row = 0
        if var in varlist[0]:
            PORfile = open(thisdir + '\\POR.txt', 'w')
            
        # len(filelines[3:]) is number of rows and nhru is number of columns
        matrix = numpy.zeros(shape=(len(filelines[3:]), nhru + 3))
        
        head = 'Dataset = ' + dataset + \
            '\nVariable = ' + var + \
            '\nRegion = ' + str(region) + \
            '\nhru = ' + str(nhru) + \
            '\n' + WFS_URL
        
        for line in filelines[3:]:
            
            splitline = line.split(',')
            timestamp = splitline[0].split('T')
            yrmoday = timestamp[0].split('-')
            year = yrmoday[0]
            month = yrmoday[1]
            day = yrmoday[2]
            # newline = year+'-'+str(month)+'-'+str(day)+' '
            newline = year + ' ' + month + ' ' + day
            print 'Year: ' + year + ', Month: ' + month + ', Day: ' + day
            # current_var_str = splitline[1:]
            current_var_float = [float(x) for x in splitline[1:]]
           
            if var == 'pr' or var == 'prcp' or var == 'Prcp':
                matrix[matrix_row, ...] = add_row_pr(var, current_var_float, newline)
                PORfile.writelines(str(year) + '-' + str(month) + '-' + str(day) + '\n')
               
                if int(year) not in years_list:
                    years_list.append(int(year))
            elif var == 'tas' or var == 'tmax' or var == 'tmin' or var == 'Tavg':
                matrix[matrix_row, ...] = add_row_temp(var, current_var_float, newline)
            else:
                print "You shouldn't enter this else statement"
               
      
            if matrix_row == 0:
                start_date = str(day) + '-' + str(month) + '-' + str(year)
                head += '\n# daily ' + start_date + ' - '
                start_day = int(day)
                start_month = int(month)
                start_year = int(year)
            matrix_row += 1
           
#            if var !='pr':
#                newline = newline +str((float(splitline[i].rstrip())*1.8)+32)+' ' # Celsius to Fahrenheit
# #            for i in range(1,len(splitline)):
# #                if var != 'pr':
# #                    newline = newline +str((float(splitline[i].rstrip())*1.8)+32)+' ' # Celsius to Fahrenheit
# #                if var == 'pr':
# #                    newline = newline +str(float(splitline[i].rstrip())*.0393)+' '# mm to inches
#             if var == 'ppt':
#                 PORline = str(year)+'-'+str(month)+'-'+str(day)+'\n'
#                 PORfile.writelines(PORline)
#                 PORcount = PORcount+1
#            newline = newline + '\n'
            end_date = str(day) + '-' + str(month) + '-' + str(year)
            end_year = int(year)
            end_month = int(month)
            end_day = int(day)
        
            
            head += end_date + '\n######'
            if var == 'pr' or var == 'prcp' or var == 'Prcp':
                numpy.savetxt(thisdir + '\\' + var + '_daily.txt', matrix, '%1.5f', ' ', header=head)
                WBM_Files.append(thisdir + '\\' + var + '_daily.txt')
            elif var == 'tmax':
                tmax = matrix
                numpy.savetxt(thisdir + '\\' + var + '_daily.txt', matrix, '%1.5f', ' ', header=head)
                WBM_Files.append(thisdir + '\\' + var + '_daily.txt')
            elif var == 'tmin':
                tmin = matrix
                numpy.savetxt(thisdir + '\\' + var + '_daily.txt', matrix, '%1.5f', ' ', header=head)
                WBM_Files.append(thisdir + '\\' + var + '_daily.txt')
            elif var == 'tas' or var == 'Tavg':
                numpy.savetxt(thisdir + '\\' + var + '_daily.txt', matrix, '%1.5f', ' ', header=head)
                WBM_Files.append(thisdir + '\\' + var + '_daily.txt')
        
        
            inputfile.close()
            print var + '_daily.txt is finished formatting'
            por = PORfile
            PORfile.close()
        
        
        if 'Tavg' not in varlist and 'tas' not in varlist:
            tave = numpy.add(tmin, tmax) / 2
            head = '# Dataset = ' + dataset + \
                '\n# Variable = tave' \
                '\n# Region = ' + str(region) + \
                '\nhru = ' + str(nhru) + \
                '\n#' + WFS_URL + \
                '\n# daily ' + start_date + ' - ' + end_date + \
                '\n######'
   
            numpy.savetxt(thisdir + '\\tave_daily.txt', tave, '%1.5f', ' ', header=head)
            WBM_Files.append(thisdir + '\\tave_daily.txt')
            varlist.append('tave')
            print 'tave_daily.txt is finished formatting'
           
        head_tave = '# Dataset = ' + dataset + \
       '\n# Variable = TAVE' \
       '\n# Region = ' + str(region) + \
       '\nhru = ' + str(nhru) + \
       '\n#' + WFS_URL + \
       '\n# daily ' + start_date + ' - ' + end_date + \
       '\n######'
       
        head_prcp = '# Dataset = ' + dataset + \
       '\n# Variable = PRCP' \
       '\n# Region = ' + str(region) + \
       '\nhru = ' + str(nhru) + \
       '\n#' + WFS_URL + \
       '\n# daily ' + start_date + ' - ' + end_date + \
       '\n######'
        
          
    timeEnd = time.time()
    osTimes2 = os.times()
    utime = osTimes2[0] - osTimes1[0]
    stime = osTimes2[1] - osTimes1[1]

    print "Clock time was %s seconds" % (timeEnd - timeStart)
    print "utime = %s, stime = %s" % (utime, stime)
                
def dailyToMonth(varlist, thisdir, years_list, months_list, nhru, head_prcp, head_tave, start_date, end_date, dataset):      
   
    for matrix in varlist:
        # file = open(thisdir + '\\' + matrix + '_daily.txt', 'r')
        file = open(thisdir + '\\' + matrix + '_daily.txt', 'r')
        # porfile = open(thisdir+'\\POR.txt', 'r')
        porfile = open(thisdir + '\\POR.txt', 'r')
        por_lines = porfile.readlines()
        # Gets year, month, and day into list
        split = por_lines[0].split('-')
#            start_year = int(split[0])
#             start_month = int(split[1])
#             start_day = int(split[2])
        filelines = file.readlines()
        for porLine in por_lines:
            split = porLine.split('-')
            
        end_year = end_date[0]
        end_month = end_date[1]
        end_day = end_date[2]
            
            
        count = 0
             
        # All the data needed to be converted to monthly     
        data_lines = filelines[7:]
        # index is the current line number
        index = 0
    
        month_days = 0
        num_months = []
        # c = -1
        for i in years_list:
            for j in months_list:
                days = str(monthrange(i, j)[1])
                if i == years_list[len(years_list) - 1] and j == 12:
                    num_months.append(float(days))
                    break
                else:
                    # Only have if/else statement for daymet
                    if i % 4 == 0 and j == 12 and dataset == 'DAYMET':
                        num_months.append(30.0)
                        # print 'leap year'
                    else:
                        num_months.append(float(days))
            
        if end_month != 12:
            length = (end_year - (years_list[0])) * 12
            length += end_month 
        else:
            length = (end_year - (years_list[0] - 1)) * 12
                
        mat = numpy.zeros(shape=(length, nhru + 2))

        for year in years_list:
            for month in months_list:
                # 2D array
                sum = numpy.zeros(nhru)
                # Number of days in current month
                days = int(num_months[month_days])
                # Loop through the current month
                for day in range(1, days + 1):
                    print 'Year: ' + str(year) + ', Month: ' + str(month) + ', Day: ' + str(day)
                    # print 'index is ' + str(index)    
                    line = data_lines[index]
                    split = line.split(' ')
                    # December of 1980 only gives 30 days
                    split = split[3:]
                        
                    index += 1
                            
                    nump_zer = numpy.zeros(nhru)                  
                    ind = 0    
                    for val in nump_zer:
                        val = split[ind]
                        nump_zer[ind] = val
                        ind += 1 
                    # print 'Sum: ' + str(sum)
                    # print 'Nump: ' + str(nump_zer)
                    sum = nump_zer + sum
                    # print 'Sum: ' + str(sum)
                            
                    # If finished with conversion   
                    if year == end_year and month == end_month and day == end_day:
                        break 
                        
                    # Need to rerun all GSD's     
                if matrix != 'prcp' and matrix != 'pr':
                    sum /= days
                
                mat[count, 0] = float(year)
                mat[count, 1] = float(month)
                mat[count, 2:] = sum
                
                count += 1
                month_days += 1
                    
                if year == end_year and month == end_month:
                    break
        if matrix == 'prcp' or matrix == 'pr':
            matrix = 'PPT'   
            numpy.savetxt(thisdir + '\\' + matrix + '_month.txt', mat, '%1.5f', ' ', header=head_prcp)

        else:
            matrix = 'TAVE'     
            numpy.savetxt(thisdir + '\\' + matrix + '_month.txt', mat, '%1.5f', ' ', header=head_tave)
        print 'Finished converting ' + matrix + '_month.txt' 

   
# Old code
#     #*************************************************************
#     # write and format final temp file
#     tmaxfile = thisdir+'\\tmax_daily.txt'
#     tminfile = thisdir+'\\tmin_daily.txt'
#     tavefile = 'TAVE_daily.txt'
#     outputfile = open (thisdir+'\\'+tavefile, 'a')
#     files = [tmaxfile,tminfile]
# 
#     tmax = numpy.zeros(shape = (PORcount,nhru))
#     tmin = numpy.zeros(shape = (PORcount,nhru))
# 
#     dateList=[]
#     for i in range (0,len(files)):
#         count = 0
#         infile = open(files[i], 'r')
#         filelines = infile.readlines()
#         for lines in filelines[0:tmax.shape[0]]:
#             items = lines.split()
#             yrmoday = items[0].split('-')
#             year = yrmoday[0]
#             month = yrmoday[1]
#             day = yrmoday[2]
#             if i == 0:
#                 tmax[count,...]=items[1:]
#             if i == 1:
#                 tmin[count,...]=items[1:]
#             newstring = year+'-'+month+'-'+day+' '
#             dateList.append(newstring)
#             count = count+1
#     infile.close()
# 
#     temp_sum = numpy.add(tmax,tmin)
#     tave = temp_sum/2
# 
#     for i in range(0,tave.shape[0]):
#         newstring = dateList[i]
#         for j in range(0,tave.shape[1]):
#             newstring = newstring+str(tave[i][j])+' '
#         newstring = newstring+'\n'
#         outputfile.writelines(newstring)
#     print 'done converting files for use in WBM'
#     outputfile.close()

    

        
        