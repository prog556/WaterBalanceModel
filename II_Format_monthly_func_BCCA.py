import csv, os,numpy
# Parse the csv file into precip and temp
tile = 'SP'
runtype = 'FC'
scenario='a2'
nhru=371

if runtype == 'CC':
    run = ''
    thisdir=os.getcwd()+"\\BCCA\\"+tile+"\\"+tile+"_"+runtype
    os.chdir(thisdir)
else:
    run = scenario
    thisdir=os.getcwd()+"\\BCCA\\"+tile+"\\"+tile+"_"+runtype+"\\"+scenario
    os.chdir(thisdir)

# set directories

#os.chdir(thisdir+'\\BCCA\\SP\\SP_FC\\'+run)
#CC
#dataset= ['cccma_cgmc3'+run,'cnrm_cm3'+run,'gfdl_cm2_1'+run,'ipsl_cm4'+run,'miroc3_2_medres'+run,'miub_echo_g'+run,'mri_cgcm2_3_2a'+run]
dataset=['mri_cgcm2_3_2a'+run]

for data in dataset:
    os.makedirs(data)
    #dataType = ['pr','tasmax','tasmin']
    varfile = [data+'-gregorian-20c3m-run1-pr-BCCA_0-125deg-monthly',\
        data+'-gregorian-20c3m-run1-tasmax-BCCA_0-125deg-monthly',\
        data+'-gregorian-20c3m-run1-tasmin-BCCA_0-125deg-monthly']
    varlist=['pr','tasmax','tasmin']
    index = 0

##    PORcount = 0
##    for var in varlist:
##        outputfile = thisdir+'\\'+data+'\\'+var+"_month.txt"
##        #inputfile=open(thisdir+'\\'+var+".csv", 'r')
##        #inputfile=open(thisdir+'\\'+data+'-gregorian-20c3m-run1-'+varlist+'-BCCA_0-125deg-monthly.csv', 'r')
##        inputfile=open(thisdir+"\\"+data+'-gregorian-20c3m-run1-'+var+'-BCCA_0-125deg-monthly.csv', 'r')
##        filelines = inputfile.readlines()
##        outputfile = open (outputfile, 'a')
##        PORfile = open(thisdir+"\\"+data+'\\POR.txt','a')
##        for line in filelines[2:]:
##            #print line[0:20]
##            splitline = line.split(',')
##            timestamp = splitline[0].split('T')
##            yrmoday = timestamp[0].split('-')
##            year = yrmoday[0]
##            month = int(yrmoday[1])
##            newline = year+' '+str(month)+' '
##            print year,month
##            for i in range(1,len(splitline)):
##                if var != 'pr':
##                    newline = newline +str((float(splitline[i].rstrip())*1.8)+32)+' ' # Celsius to Fahrenheit
##                if var == 'pr':
##                    newline = newline +str(float(splitline[i].rstrip())*.0393)+' '# mm to inches
##                # K to C
##                # K - 273.15 - deg C
##                # Celsius to Fahrenheit
##                #if var != 'ppt':
##                    #newline = newline +str((float(splitline[i].rstrip())*1.8)+32)+' '
##                # K to F
##                #K * 1.8 - 459.67
##                #newline = newline +str((float(splitline[i].rstrip())*1.8)-459.67)+' '
##                # kg m-2 s-1 to mm/day
##                # (kg m-2 s-1)*8640 to in/day
##                #newline = newline +str(float(splitline[i].rstrip())*8640*.3937)+' '
##                # mm to inches
####                if var == 'ppt':
####                    newline = newline +str(float(splitline[i].rstrip())*.0393)+' '
##            if var == 'pr':
##                PORline = str(year)+'-'+str(month)+'-01 \n'
##                PORfile.writelines(PORline)
##                PORcount = PORcount+1
##            newline = newline + '\n'
##            outputfile.writelines(newline)
##        inputfile.close()
##        outputfile.close()
##        print var+'.txt is finished formatting'
##    PORfile.close()
##    #*************************************************************
##        # write and format final temp file
##    tmaxfile = thisdir+'\\'+data+'\\tasmax_month.txt'
##    tminfile = thisdir+'\\'+data+'\\tasmin_month.txt'
##    tavefile = 'TAVE_month.txt'
##    outputfile = open (thisdir+'\\'+data+'\\'+tavefile, 'a')
##    files = [tmaxfile,tminfile]
##
##    tmax = numpy.zeros(shape = (PORcount,nhru))
##    tmin = numpy.zeros(shape = (PORcount,nhru))
##
##    dateList=[]
##    for i in range (0,len(files)):
##        count = 0
##        infile = open(files[i], 'r')
##        filelines = infile.readlines()
##        for lines in filelines[0:tmax.shape[0]]:
##            items = lines.split()
##            if i == 0:
##                tmax[count,...]=items[2:]
##            if i == 1:
##                tmin[count,...]=items[2:]
##            newstring = items[0]+' '+items[1]+' '
##            dateList.append(newstring)
##            count = count+1
##    infile.close()
##
##    temp_sum = numpy.add(tmax,tmin)
##    tave = temp_sum/2
##
##    for i in range(0,tave.shape[0]):
##        newstring = dateList[i]
##        for j in range(0,tave.shape[1]):
##            newstring = newstring+str(tave[i][j])+' '
##        newstring = newstring+'\n'
##        outputfile.writelines(newstring)
##    print 'done converting files for use in WBM'
##    outputfile.close()