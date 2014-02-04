# 1_WBM_main.py
#
# ---------------------------------------------------------------------------
# Accompanying scripts and order they are run
# ---------------------------------------------------------------------------

# Import system modules
import os, numpy, sys, traceback

# Import the other four scripts, each containing a function
# we an combine all five scripts into one if that is desireable
import II_Format_monthly_func
import II_Format_daily_func

# traceback for messages, need to check to see if this
# works with functions
def trace():
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    line = tbinfo.split(", ")[1]
    filename = sys.path[0] + os.sep + "1_WBM_main.py"
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror



def main_func(region, tile, nhru, dataset, csvs):
    try:
#         #region = '13'
#         region = Step1.getRegion()
#         #tile = ''
#         tile = Step1.getTile()
#         #number of hrus
#         #nhru = 1958
#         nhru = Step1.getNHRU()
#     
#         # dataset to process
#         #dataset='PRISM'
#         dataset = Step1.getDataSet()
        # Instead of using these, you might want to recall the daily/monthly list value you wrote in pyGDP
        # from the dataset properties
        daily = ['Gridded_Observed_Data_1950_1999','Gridded_Observed_Data_1949_2010','DAYMET']
        monthly = ['PRISM','GFDL_CM_2_0','GENMON','MPI_ECHAM5','NOAA_NCEP']
    
        if dataset in monthly:
            II_Format_monthly_func.Format_monthly(numpy,region,tile,dataset,nhru, csvs)
    
        if dataset in daily:
            II_Format_daily_func.Format_daily(numpy,region,tile,dataset,nhru)
    # don't worry about code below here now unti lwe get the frist two functions in VisTrails
    ##        Rscript = 'C:/Program Files/R/R-3.0.0/bin/Rscript.exe'
    ##        Rcode = 'D:/abock/Water_Balance/Step1_CLIMATE_DATA\monthly_summary.R'
    ##        retcode = subprocess.call([Rscript,Rcode])
    ##        if retcode != 0:
    ##            print 'something wrong with the R script'
    
    # Return any PYTHON or system specific errors#
    except:
        line, filename, err = trace()
        print "Error on line " + line + " of the file: " + filename + " with the error: " + err
#         arcpy.AddError("Python error on " + line + " of " + filename)
#         arcpy.AddError(err)
    
    finally:
        # Print a message
        print "kaput"


# main_func()










