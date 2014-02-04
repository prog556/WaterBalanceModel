import os, csv

os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\R11\\SBDDS\\DAYMET2')

read = csv.reader(open("tmin.csv", 'rb'))

write = csv.writer(open('tmin_PARSE.csv', 'wb'))

index = 0

var = read.next()

gage = read.next()

type = read.next()

write.writerow(var)
write.writerow(gage)
write.writerow(type)

for row in read:
    line = row[0].split('-')
    line[0] = int(line[0])
    if line[0] <= 1983:
        write.writerow(row)
    else:
        break

