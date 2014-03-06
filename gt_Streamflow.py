'''

demo of plotting a matplotlib hydrograph from a nwis data call
Created on Mar 6, 2014

@author: talbertc,abock
'''
import urllib, pickle, numpy, csv, os, datetime
from datetime import datetime, date, timedelta, time
# need urllib to get streamflow data from NWIS (website parsing module)
import urllib

import matplotlib.pyplot as plt

def plot_hydrograph(gageid, start_date, end_date):
    dates, flows = get_nwis_data(gageid, start_date, end_date)

    font = {'family' : 'serif',
        'color'  : 'darkred',
        'weight' : 'normal',
        'size'   : 16,
        }

    plt.plot([datetime.strptime(d, "%Y-%m-%d") for d in dates], flows, 'k')
    plt.title('Flow at: ' + str(gageid), fontdict=font)
    plt.xlabel('date', fontdict=font)
    plt.ylabel('flow (cfs)', fontdict=font)

    #  Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.show()

thisdir = os.getcwd()

# determines number of days between two dates
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

def date_to_urldate(indate):
    '''converts a py date to a string representation needed by
    the nwis site
    '''
    return "-".join([str(indate.year), str(indate.month), str(indate.day)])

def get_nwis_data(gageid, start_date, end_date):
    '''
    '''
    years = []
    months = []
    days = []
    for result in perdelta(start_date, end_date, timedelta(days=1)):
        dt = datetime.strptime(str(result), "%Y-%m-%d")
        t = dt.timetuple()
        years.append(t[0])
        months.append(t[1])
        days.append(t[2])

    #  make empty matrix for holding flows
    delta = d0 - d1
    flows = numpy.zeros(shape=(abs(delta.days), 4))
    #flows.fill(NaN)  #  make NaN for all
    flows[:]=numpy.nan
    flows[..., 0] = years
    flows[..., 1] = months
    flows[..., 2] = days

    print "Going to the NWIS web services for each gage."
    # these are codes that explain where there streamgage data did not meet
    # the QA/QC check
    noDataList=['Ice','Eqp','Bkw','Rat','Dis','Ssn','Mnt','***']

    # get streamgage name, can get other station properties this way too.
    gagepage = urllib.urlopen('http://waterdata.usgs.gov/nwis/inventory?search_site_no='+gageid+'&search_site_no_match_type=exact&group_key=NONE&format=sitefile_output&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&list_of_search_criteria=search_site_no')
    for line in gagepage:
        if len(line)>1:
            if line[3:13]=='station_nm':
                line = line.replace(' <station_nm>','')
                line = line.replace('</station_nm>\n','')
                if line !=' ':
                    Sta_name=line

    # codes 0.00_ZFl, Zfl - zero flow
    usock = urllib.urlopen('http://waterdata.usgs.gov/nwis/dv?referred_module=sw&search_site_no='+gageid+'&search_site_no_match_type=exact&site_tp_cd=ST&index_pmcode_30208=1&index_pmcode_00060=1&index_pmcode_99060=1&sort_key=site_no&group_key=NONE&sitefile_output_format=xml&column_name=agency_cd&column_name=site_no&column_name=station_nm&range_selection=date_range&begin_date='+str(d0_url)+'&end_date='+str(d1_url)+'&format=rdb&date_format=YYYY-MM-DD&rdb_compression=value&list_of_search_criteria=search_site_no%2Csite_tp_cd%2Crealtime_parameter_selection')
    dateList=[]
    flowList=[]
    count=0
    for line in usock:
        if line !='\n':
            items = line.split()
        if items[0]=='USGS':
            dateList.append(items[2])
            if len(items)<4:
                flowList.append(-999)
            else:
                if items[3]=='0.00_ZFl':
                    flowList.append(0)
                if items[3]=='ZFl':
                    print 'ZFl'
                    flowList.append(0)
                elif items[3] in noDataList:
                    flowList.append(-999)
                else:
                    flowList.append(items[3])
    # convert strings to float
    # this may throw an exception if there is a QAQC code (aka line 146) that has slipped through
    flowList_float=[float(x) for x in flowList]
    flowListnp=numpy.array(flowList_float)
    flowListnp[flowListnp==-999]=numpy.nan

    # this piece of code places the streamflow data into the matrix
    # this is important because the streamflow data may begin/end inside matrix
    if len(dateList)>0:
        first_day=dateList[0].split('-')
        date_integer=[int(x) for x in first_day]
        date_format = date(date_integer[0],date_integer[1],date_integer[2])
        delta = d0 - date_format
        #print delta.days
        if delta.days!=0:
            placer = abs(delta.days)
        if delta.days==0:
            placer=0
        len(flowList_float)
        print placer
        flows[placer:len(flowList_float)+placer,3]=flowList_float
    else:
        flows[...,i]=-999
    flows[flows==-999.0]=numpy.nan
    # save to daily textfile
    numpy.savetxt(wkdir+r'/Flows_daily.txt', flows, fmt='%s',delimiter=' ')

    #convert from daily cfs to monthly (mm)
    streamflowfile= open(wkdir+r'/Flows_monthly.txt','w')
    for i in range(min(years),max(years)+1):
        for j in range(1,13):
            month=flows[(flows[:,0]==i)&(flows[:,1]==j)]
            #mask nan values from monthly mean calculation
            mask_month = numpy.ma.masked_array(month[:,3],numpy.isnan(month[:,3]))
            #arr = numpy.ma.array(0,flows,1)
            if (numpy.ma.max(mask_month)is numpy.ma.masked)==False:
                month_mean=numpy.mean(mask_month)
                month_mean_mm=((month_mean/float(areakm2))*2.446514*len(mask_month))
                month_mean_mm=round(month_mean_mm,2)
            else:
                month_mean_mm='NA'
            #print month_mean
            newline = str(years[i])+' '+str(j)+' '+str(month_mean_mm)+'\n'
            streamflowfile.writelines(newline)
    streamflowfile.close()
    return dateList, flowListnp

if __name__ == '__main__':
    #  set parameters
    gageid = '06746095'
#   pick the dates that you are interested in getting streamflow for
    d0 = date(1949, 1, 1)
    d0_url = "1949-01-01"
    d1 = date(2013, 12, 31)
    d1_url = "2013-12-31"
    wkdir = 'D:/abock/temp'
    # will have to get this from one of the other steps
    areakm2 = 8.12

    plot_hydrograph(gageid, d0, d1)

'''alternative way to get date (depends on what Andy N. handles input ports)'''
#    # produce start and end dates
#    if len(str(m0))==1:
#        m0_str='0'+str(m0)
#    if len(str(m1))==1:
#        m1_str='0'+str(m1)
#    else:
#        m1_str = str(m1)
#    d0 = date(y0,m0,1)
#    d0_url = str(y0)+'-'+m0_str+'-01'
#    d1 = date(y1,m1,31)
#    d1_url = str(y1)+'-'+m1_str+'-31'
