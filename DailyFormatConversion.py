import os, numpy
from calendar import monthrange

os.chdir(os.getcwd()+'\\Step1_CLIMATE_DATA\\R11\\SBDDS\\DAYMET2')
thisdir = os.getcwd()

varlist = ['prcp', 'tmax', 'tmin', 'tave']

nhru = 7373

years_list = []
yr = 1980
while yr <= 1983:
    years_list.append(yr)
    yr += 1
months_list = [1, 2, 3, 4, 5, 6, 7, 8 , 9, 10, 11, 12]

head = '# Dataset = ' + "Daymet" + \
'\n# Variable = tave' \
'\n# Region = ' + str('R06') + \
'\nhru = ' + str(nhru) + \
'\n#' + 'https://www.sciencebase.gov/catalogMaps/mapping/ows/51d75296e4b055e0afd5be2c' + \
'\n# daily ' + '01-01-1980' + ' - ' + '01-01-1985' + \
'\n######'
        
for matrix in varlist:
    if matrix == 'prcp' or matrix == 'tave':
        #file = open(thisdir + '\\' + matrix + '_daily.txt', 'r')
        file = open(thisdir + '\\' + matrix + '_daily.txt', 'r')
        #porfile = open(thisdir+'\\POR.txt', 'r')
        porfile = open(thisdir+'\\POR.txt', 'r')
        por_lines = porfile.readlines()
        #Gets year, month, and day into list
        split = por_lines[0].split('-')
        start_year = int(split[0])
        start_month = int(split[1])
        start_day = int(split[2])
        filelines = file.readlines()
        for porLine in por_lines:
            split = porLine.split('-')
        #end_year = int(split[0])
        #end_month = int(split[1])
        #end_day = int(split[2])
        
        end_year = 1983
        end_month = 12
        end_day = 31
        
        
        count = 0
         
        #All the data needed to be converted to monthly     
        data_lines = filelines[7:]
        #index is the current line number
        index = 0

        month_days = 0
        num_months = []
        for i in years_list:
            for j in months_list:
                days = str(monthrange(i,j)[1])
                if i == years_list[len(years_list)-1] and j == 12:
                    num_months.append(float(days))
                    break
                else:
                    num_months.append(int(days))
                    
        
        if end_month != 12:
            length = (end_year-(start_year))*12
            length += end_month 
        else:
            length = (end_year-(start_year-1))*12
            
        mat = numpy.zeros(shape = (length, nhru+2))
        
        
        
        
        for year in years_list:
            print year
            for month in months_list:
                #2D array
                sum = numpy.zeros(nhru)
                #Number of days in current month
                days = int(num_months[month_days])
                    
                #Loop through the current month
                for day in range(1, days+1):
                    if not(day == 31 and year == 1980 and month == 12):
                        #print 'index is ' + str(index)    
                        line = data_lines[index]
                        split = line.split(' ')
                        temp = str(day)+'.00000'
                        #December of 1980 only gives 30 days
                        if split[2] != temp:
                            print 'stop here'
                        split = split[3:]
                        
                        index += 1
                            
                        nump_zer = numpy.zeros(nhru)                  
                        ind = 0    
                        for val in nump_zer:
                            val = split[ind]
                            nump_zer[ind] = val
                            ind += 1 
                        sum += nump_zer
                            
                        #If finished with conversion   
                        if year == end_year and month == end_month and day == end_day:
                            break 
                    
                if matrix != 'prcp':
                    sum /= days
            
                mat[count, 0] = float(year)
                mat[count, 1] = float(month)
                mat[count, 2:] = sum
            
                count += 1
                month_days += 1
                
                if year == end_year and month == end_month:
                    break
        if matrix == 'prcp':
            matrix = 'PPT'   
        else:
            matrix = 'TAVE'     
        numpy.savetxt(thisdir + '\\' + matrix+'_month.txt', mat, '%1.5f', ' ', header = head)
        print 'Finished converting ' + matrix + '.txt'