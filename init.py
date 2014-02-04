#import core.modules.module_registry
#from core.modules.vistrails_module import Module, ModuleError
from core.modules.vistrails_module import Module
from core.modules.module_registry import get_module_registry

import II_Format_daily_func
import II_Format_monthly_func, zipFormattedData, csvParse
import mows_pyGDP_BCCA_CC, mows_pyGDP_BCCA_FC, mows_pyGDP_SBDDS, mows_pyGDP_MAURERBREKE




class mows_pyGDP(Module):

    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'), 
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ('Call File', '(edu.utah.sci.vistrails.basic:String)'),
                    ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
                    ('Start Time', '(edu.utah.sci.vistrails.basic:String)'),
                    ("Scenarios", '(edu.utah.sci.vistrails.basic:List)'),
                    ('End Time', '(edu.utah.sci.vistrails.basic:String)')
                    ]
    _output_ports = [('Region', '(edu.utah.sci.vistrails.basic:String)'),
                     ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
                     ('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
                     ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                     ('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
                     ('Call File', '(edu.utah.sci.vistrails.basic:String)'),
                     ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                     ('DataType', '(edu.utah.sci.vistrails.basic:List)'),
                     ('WFS_URL', '(edu.utah.sci.vistrails.basic:String)')
                     ]

    def compute(self):
        #How to find tile, NHRU?
        region = self.getInputFromPort("Region")
        #tile = self.getInputFromPort("Tile")
        curdir = self.getInputFromPort("Directory")
        self.setResult("Directory", curdir)
        callfile = self.getInputFromPort("Call File")
        #start = self.getInputFromPort("Start Time")
        #end = self.getInputFromPort("End Time")
         
        self.setResult("Region", region)
        #Ex: SBDDS
        self.setResult("Call File", callfile)
         
        if callfile == 'BCCA_CC':
            pyGDP_data = ['cccma_cgcm3', 'cnrm_cm3', 'gfdl_cm2_1', 'ipsl_cm4', 'miroc3_2_medres', 
                          'miub_echo_g', 'mpi_echam5', 'mri_cgcm2_3_2a']
            for dt in pyGDP_data:
                mows_pyGDP_BCCA_CC.main_func(curdir.name, dt, region)
                #Dataset ex: GENMON
                self.setResult("DataSet", dt)
                #Datatype ex: RT, TA
                self.setResult("DataType", mows_pyGDP_BCCA_CC.vt_datatype)
                self.setResult("nhru", mows_pyGDP_BCCA_CC.nhru)
                #Timestep ex: Daily
                self.setResult("Timestep", mows_pyGDP_BCCA_CC.length)

           
        elif callfile == 'SBDDS':
            pyGDP_data = ['PRISM', 'DAYMET']# 'MPI_ECHAM5', 'GENMON', 'GFDL_CM_2_0', 'NOAA_NCEP', 'GSD', 'DAYMET']
            for dt in pyGDP_data:
                mows_pyGDP_SBDDS.main_func(curdir.name, dt, region)
                #Dataset ex: GENMON
                self.setResult("DataSet", dt)
                #Datatype ex: RT, TA
                self.setResult("DataType", mows_pyGDP_SBDDS.vt_datatype)
                self.setResult("nhru", mows_pyGDP_SBDDS.nhru)
                #Timestep ex: Daily
                self.setResult("Timestep", mows_pyGDP_SBDDS.length)
                self.setResult("WFS_URL", mows_pyGDP_SBDDS.url)
            
class Parse(Module):
    
    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
                    ("DataSet", '(edu.utah.sci.vistrails.basic:String)'),
                    ("DataType", '(edu.utah.sci.vistrails.basic:List)'),
                    ("Call File", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
                    ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                    ("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
                    ('Timestep', '(edu.utah.sci.vistrails.basic:String)')
                    ]
    
    _output_ports = [('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
                     ('Region', '(edu.utah.sci.vistrails.basic:String)'),
                     ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                     ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
                    ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                    ("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
                    ('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
                    ("Call File", '(edu.utah.sci.vistrails.basic:String)')
                     ]
    
    def compute(self):
        
        region = self.getInputFromPort("Region")
        dataset = self.getInputFromPort("DataSet")
        dataType = self.getInputFromPort("DataType")
        callfile = self.getInputFromPort("Call File")
        curdir = self.getInputFromPort("Directory")
        
        time = self.getInputFromPort("Timestep")
        self.setResult("Timestep", time)
        WFS_URL = self.getInputFromPort("WFS_URL")
        self.setResult("WFS_URL", WFS_URL)
        nhru = self.getInputFromPort("nhru")
        self.setResult("nhru", nhru)
        callFile = self.getInputFromPort("Call File")
        self.setResult("Call File", callFile)
        
        self.setResult("Region", region)
        self.setResult("DataSet", dataset)
        self.setResult("Directory", curdir)
        

        csvParse.main_func(region, dataset, dataType, callfile, curdir.name)
        
class Step1(Module):
    
    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
                    ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
                    ('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
                    ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                    ("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
                    ('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ("Call File", '(edu.utah.sci.vistrails.basic:String)')
                    ]
    _output_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
                     ("Call File", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Scenario", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ("DataSet", '(edu.utah.sci.vistrails.basic:String)')
                     ]
    
    def compute(self):
        
        #What directory would the input csv's be at?
        callFile = self.getInputFromPort("Call File")
        self.setResult("Call File", callFile)
        region = self.getInputFromPort("Region")
        self.setResult("Region", region)
        #tile = self.getInputFromPort("Tile")
        nhru = self.getInputFromPort("nhru")
        dataset = self.getInputFromPort("DataSet")
        self.setResult("DataSet", dataset)
        WFS_URL = self.getInputFromPort("WFS_URL")
        time = self.getInputFromPort("Timestep")
        curdir = self.getInputFromPort("Directory")
        self.setResult("Directory", curdir)  
        
             
         
        if time == 'Monthly':
            II_Format_monthly_func.Format_monthly(region,'',dataset, nhru, WFS_URL, curdir.name)
        elif time == 'Daily':
            II_Format_daily_func.Format_daily(region, '', dataset, nhru, WFS_URL, curdir.name)
       
class ZipData(Module):
    
    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
                    ("DataSet", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Call File", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Scenario", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)')
                    ] 
           
    _output_ports = [('Zip File', '(edu.utah.sci.vistrails.basic:File)')]
        
        
    def compute(self):
        
        region = self.getInputFromPort("Region")
        dataset = self.getInputFromPort("DataSet")
        callFile = self.getInputFromPort("Call File")
        #scenario = self.getInputFromPort("Scenario")
        curdir = self.getInputFromPort("Directory")
        
        zipFormattedData.main_func('', region, callFile, dataset, curdir.name)
        self.setResult("Zip File", zipFormattedData.zipfile)
###############################################################################



def initialize(*args, **keywords):
    
    mows_pygdp = get_module_registry()
    mows_pygdp.add_module(mows_pyGDP)
    
    step1 = get_module_registry()
    step1.add_module(Step1)
    
    parse = get_module_registry()
    parse.add_module(Parse)
    
    zipData = get_module_registry()
    zipData.add_module(ZipData)




