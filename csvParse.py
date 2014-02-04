import csv, os

global parsedFiles

parsedFiles = []
#dataset: ex GENMON
#dataType: ex RT, TA
#data: ex SBDDS
def main_func(region, dataset, dataType, callfile, curdir):
    # Parse the csv file into precip and temp

    
    os.chdir(curdir+'\\'+dataset)
    
    csvread = csv.reader(open(region+'_'+dataset+'.csv', 'rb'))
    csvwrite = csv.writer(open(dataType[0]+'.csv', "wb"))
    #parsedFiles.append(csvwrite)
    
    #Parse the csv file 
    index = 0
    #parsedFiles = []
    
    temp = csvread
    var = temp.next()
    var[0] = '#'+dataType[0]
    #Gets gage ids
    gage = temp.next()
    
    #Writes current variable to csv file
    #csvwrite.writerow(callfile)
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
                        csvwrite.writerow(csvread.next())
                    else:
                        #If SBDDS use next line of csvread.next()
                        #Eitherwise, comment it out
                        csvread.next()
                        csvwrite.writerow(csvread.next())
                        #csvwrite.writerow(csvread.next())
                    break
                else:
                    if dataType[index+1] not in row[0] and row[0] not in dataType[index+1]:
                        csvwrite.writerow(row)
         
        parsedFiles.append(os.getcwd()+'\\'+variable+'.csv')           
        print "Finished parsing " + variable + ".csv"
        # use index to keep track of next variable
        if (index + 1) < len(dataType):
            index += 1 
            
            
            
#main_func();