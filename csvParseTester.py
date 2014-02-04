import csvParse, csv, os

os.chdir('C:\\Users\\reimandy\\Documents\\pyGDP')


csvParse.main_func(csv.reader(open('R06_NOAA NCEP.csv', 'rb')), ['RT', 'TA'])
csvParse.main_func(csv.reader(open('R06_GFDL CM 2.0.csv', 'rb')), ['RT', 'TA'])
csvParse.main_func(csv.reader(open('R06_GENMON.csv', 'rb')), ['RT', 'TA'])
csvParse.main_func(csv.reader(open('R06_MPI ECHAM5.csv', 'rb')), ['RT', 'TA'])
csvParse.main_func(csv.reader(open('R06_PRISM.csv', 'rb')), ['ppt', 'tmx', 'tmn'])
csvParse.main_func(csv.reader(open('R06_DAYMET.csv', 'rb')), ['prcp', 'tmax', 'tmin'])
csvParse.main_func(csv.reader(open('R06_Gridded Observed Data(1949-2010).csv', 'rb')), ['Prcp', 'Tavg'])





