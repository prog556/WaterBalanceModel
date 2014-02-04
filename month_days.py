nodays=[]

dataset='BCCA'
scenario='_cc'

outfile = open('D:\\abock\\Water_Balance\\Step1_CLIMATE_DATA\\BCCA\\'+dataset+scenario,'w')

# Perform this operation only for precipitation variables
# 1 - decompose start and end date dataset properties to get startyear and startmonth, endmonth, endyear
# 2 - write an if/else to perform monthly conversions for specific datasets (all monthly with units mm/day)
#   maybe add as one more dataset property to list??
# 3 - create a numpy of array, single dimension, length = number of months
#   create numpy array similar to numpy matrix
#   function called numpy vstack (vertical stack) hstack (horizontal stack) -> append to a matrix or array
# 4 - multiply the matrix by the numpy array, try to first use a function similar to this:
#   new_precip_matrix (mm/month) = [column(mm/days)*conversion(days) for column in precip_matrix]
#   or try numpy.multiply

# IMOPORTANT:  Keep in mind the BCCA future conditions datasets, the period of record
# goes from 2046-2065, then skips from 2081-2100 or something like that

#dataset=BCCA, cccma_cgmc3, 2046-2100
if scenario=='_cc':
    dayfile = open
    from calendar import monthrange
    for i in range(startyear,endyear+1): # range accounting = last item +1
        for j in range(starmonth,endmonth+1):
            print monthrange(i,j)
            nodays = str(monthrange(i,j)[1])
            if i==2000 and j ==12:
                outfile.close()
            else:
                outfile.writelines(nodays+'\n')
    outfile.close()

