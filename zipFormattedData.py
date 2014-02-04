import os, zipfile

global zipFile

def main_func(scenario, region, callFile, dataset, curdir):
    
    def zipShapefile(inlist, newZipFN, region): 
        if (os.path.exists(newZipFN)):
                print 'Deleting '+newZipFN
                os.remove(newZipFN)
         
        if (os.path.exists(newZipFN)):
            print 'Unable to Delete'+newZipFN
            return False
        
        splt = newZipFN.split('_')
        #scen is used for determining the scenario of dataset
        #scen = splt.split('.')
        
        #os.chdir(os.getcwd()+'\\'+splt[1])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_CC\\'+split[0])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\SBDDS\\'+split[1])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_FC\\a2\\'+split[0])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\BCCA_FC\\a1b\\'+split[0])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\MAURERBREKE\\a2\\'+split[1])
        #os.chdir('C:\\Users\\reimandy\\workspace\\userpackages\\WaterBalanceModel\\Step1_CLIMATE_DATA\\'+region+'\\MAURERBREKE\\'+scen[0]+'\\'+split[1])
        zipobj = zipfile.ZipFile(newZipFN,'w')
        
        for val in inlist:
            if not (os.path.exists(val)):
                print val + ' Does Not Exist'
                return False
        
        for infile in inlist:#glob.glob(infile+'_month.txt'):
            print "Writing "+infile+' to '+newZipFN
            zipobj.write(infile,infile,zipfile.ZIP_DEFLATED)
            
        print "Writing POR.txt to " + newZipFN
        zipobj.write("POR.txt",'POR.txt', zipfile.ZIP_DEFLATED)
        zipobj.close()
        return True
    
    files = ['PPT_month.txt', 'TAVE_month.txt']
    
    #MAURERBREKE
    #sets = ['cccma-cgcm3-1_1', 'gfdl-cm2-1_1','miroc3-2-medres_1', 'miub-echo-g_1', 'mpi-echam5_1', 'mri-cgcm2-3-2a_1']
    
    #SBDDS
    
    os.chdir(curdir+'\\'+dataset)
    #for data in sets:
    print 'zipping up formatted data for:\n\tRegion: ' + region + '\n\tpyGDP: '+  callFile + '\n\tDataSet: ' + dataset
    zipShapefile(files, 'Formatted Data: ' + callFile + '_' + region+'_'+dataset+'.zip', region)  
    print 'Data zipped up\n'

#main_func()