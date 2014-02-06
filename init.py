#import core.modules.module_registry
#from core.modules.vistrails_module import Module, ModuleError
from core.modules.vistrails_module import Module
from core.modules.module_registry import get_module_registry

import os
 
import II_Format_daily_func, II_Format_monthly_func, zipFormattedData, csvParse
import mows_pyGDP_BCCA_CC, mows_pyGDP_BCCA_FC, mows_pyGDP_SBDDS, mows_pyGDP_MAURERBREKE




class mows_pyGDP(Module):

    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'), 
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ('Format File', '(edu.utah.sci.vistrails.basic:String)'),
                    ("DataSet", '(edu.utah.sci.vistrails.basic:String)'),
                    #('Start Time', '(edu.utah.sci.vistrails.basic:String)'),
                    #("Scenarios", '(edu.utah.sci.vistrails.basic:List)'),
                    #('End Time', '(edu.utah.sci.vistrails.basic:String)')
                    ]
    _output_ports = [#('Region', '(edu.utah.sci.vistrails.basic:String)'),
                     #('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
                     #('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                     #('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
                     #('Format File', '(edu.utah.sci.vistrails.basic:String)'),
                     ("pyGDP List", '(edu.utah.sci.vistrails.basic:List)'),
                     ("Directory", '(edu.utah.sci.vistrails.basic:Directory)')
                     #('DataType', '(edu.utah.sci.vistrails.basic:List)'),
                     #('WFS_URL', '(edu.utah.sci.vistrails.basic:String)')
                     ]

    def compute(self):
        
        
        
        region = self.getInputFromPort("Region")
        dataset = self.getInputFromPort("DataSet")
        curdir = self.getInputFromPort("Directory")
        self.setResult("Directory", curdir)
        format_file = self.getInputFromPort("Format File")
        #start = self.getInputFromPort("Start Time")
        #end = self.getInputFromPort("End Time")
        
        
        self.setResult("Region", region)
        #Ex: SBDDS
        self.setResult("Format File", format_file)
        
        directories = [region, format_file, dataset]
        os.chdir(curdir.name)
        
        for dct in directories:
            file_loc = os.getcwd()+'\\'+dct
            if not os.path.exists(file_loc):
                os.mkdir(file_loc)
            os.chdir(file_loc)
        
        
#         if format_file == 'BCCA_CC':
#             mows_pyGDP_BCCA_CC.main_func(curdir.name, dt, region)
#             #Dataset ex: GENMON
#             self.setResult("DataSet", dt)
#             #Datatype ex: RT, TA
#             self.setResult("DataType", mows_pyGDP_BCCA_CC.vt_datatype)
#             self.setResult("nhru", mows_pyGDP_BCCA_CC.nhru)
#             #Timestep ex: Daily
#             self.setResult("Timestep", mows_pyGDP_BCCA_CC.length)
        def list_define():
            vt_list = []
            vt_list.append(region)
            vt_list.append(dataset)
            vt_list.append(format_file)
            vt_list.append(mows_pyGDP_SBDDS.vt_datatype)
            vt_list.append(mows_pyGDP_SBDDS.nhru)
            vt_list.append(mows_pyGDP_SBDDS.length)
            vt_list.append(mows_pyGDP_SBDDS.url)
            return vt_list
           
        if format_file == 'SBDDS':
            mows_pyGDP_SBDDS.main_func(os.getcwd(), dataset, region)
            #Dataset ex: GENMON
            #self.setResult("DataSet", dataset)
            #Datatype ex: RT, TA
            #self.setResult("DataType", mows_pyGDP_SBDDS.vt_datatype)
            #self.setResult("nhru", mows_pyGDP_SBDDS.nhru)
            #Timestep ex: Daily
            #self.setResult("Timestep", mows_pyGDP_SBDDS.length)
            #self.setResult("WFS_URL", mows_pyGDP_SBDDS.url)
            csvParse.main_func(region, dataset, mows_pyGDP_SBDDS.vt_datatype, format_file, os.getcwd())
            self.setResult("pyGDP List", list_define())
               
            
# class Parse(Module):
#     
#     _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
#                     ("DataSet", '(edu.utah.sci.vistrails.basic:String)'),
#                     ("DataType", '(edu.utah.sci.vistrails.basic:List)'),
#                     ("Format File", '(edu.utah.sci.vistrails.basic:String)'),
#                     ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
#                     ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
#                     ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
#                     ("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
#                     ('Timestep', '(edu.utah.sci.vistrails.basic:String)')
#                     ]
#     
#     _output_ports = [('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
#                      ('Region', '(edu.utah.sci.vistrails.basic:String)'),
#                      ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
#                      ('Tile', '(edu.utah.sci.vistrails.basic:String)'),
#                     ('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
#                     ("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
#                     ('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
#                     ("Format File", '(edu.utah.sci.vistrails.basic:String)')
#                      ]
#     
#     def compute(self):
#         
#         region = self.getInputFromPort("Region")
#         dataset = self.getInputFromPort("DataSet")
#         dataType = self.getInputFromPort("DataType")
#         format_file = self.getInputFromPort("Format File")
#         curdir = self.getInputFromPort("Directory")
#         
#         time = self.getInputFromPort("Timestep")
#         self.setResult("Timestep", time)
#         WFS_URL = self.getInputFromPort("WFS_URL")
#         self.setResult("WFS_URL", WFS_URL)
#         nhru = self.getInputFromPort("nhru")
#         self.setResult("nhru", nhru)
#         format_file = self.getInputFromPort("Format File")
#         self.setResult("Format File", format_file)
#         
#         self.setResult("Region", region)
#         self.setResult("DataSet", dataset)
#         self.setResult("Directory", curdir)
#         
# 
#         csvParse.main_func(region, dataset, dataType, format_file, curdir.name)
        
class FormatStep(Module):
    
    _input_ports = [#("Region", '(edu.utah.sci.vistrails.basic:String)'),
                    #('DataSet', '(edu.utah.sci.vistrails.basic:String)'),
                    #('nhru', '(edu.utah.sci.vistrails.basic:Float)'),
                    #("WFS_URL", '(edu.utah.sci.vistrails.basic:String)'),
                    #('Timestep', '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)'),
                    ("pyGDP List", '(edu.utah.sci.vistrails.basic:List)')
                    #("Format File", '(edu.utah.sci.vistrails.basic:String)')
                    ]
    _output_ports = [("pyGDP List", '(edu.utah.sci.vistrails.basic:List)')
                     #("Region", '(edu.utah.sci.vistrails.basic:String)'),
                     #("Format File", '(edu.utah.sci.vistrails.basic:String)'),
                    #("Scenario", '(edu.utah.sci.vistrails.basic:String)'),
                    ("Directory", '(edu.utah.sci.vistrails.basic:Directory)')
                    #("DataSet", '(edu.utah.sci.vistrails.basic:String)')
                     ]
    
    def compute(self):
        
        #What directory would the input csv's be at?
#         format_file = self.getInputFromPort("Format File")
#         self.setResult("Format File", format_file)
#         region = self.getInputFromPort("Region")
#         self.setResult("Region", region)
#         #tile = self.getInputFromPort("Tile")
#         nhru = self.getInputFromPort("nhru")
#         dataset = self.getInputFromPort("DataSet")
#         self.setResult("DataSet", dataset)
#         WFS_URL = self.getInputFromPort("WFS_URL")
#         time = self.getInputFromPort("Timestep")
#         curdir = self.getInputFromPort("Directory")
#         self.setResult("Directory", curdir)  
        pyGDP_list = self.getInputFromPort("pyGDP List")
        time = pyGDP_list[5]
        region = pyGDP_list[0]
        dataset = pyGDP_list[1]
        nhru = pyGDP_list[4]
        url = pyGDP_list[6]
        
        if time == 'Monthly':
            II_Format_monthly_func.Format_monthly(region,dataset, nhru, url, os.getcwd())
        elif time == 'Daily':
            II_Format_daily_func.Format_daily(region, dataset, nhru, url, os.getcwd())
      
class ZipData(Module):
   
    _input_ports = [("Region", '(edu.utah.sci.vistrails.basic:String)'),
                       ("DataSet", '(edu.utah.sci.vistrails.basic:String)'),
                       ("Format File", '(edu.utah.sci.vistrails.basic:String)'),
                       ("Scenario", '(edu.utah.sci.vistrails.basic:String)'),
                       ("Directory", '(edu.utah.sci.vistrails.basic:Directory)')
                       ] 
              
    _output_ports = []
           
           
    def compute(self):
        region = self.getInputFromPort("Region")
        dataset = self.getInputFromPort("DataSet")
        format_file = self.getInputFromPort("Format File")
        scenario = self.getInputFromPort("Scenario")
        curdir = self.getInputFromPort("Directory")
       
        zipFormattedData.main_func('', region, format_file, dataset, curdir.name)
        self.setResult("Zip File", zipFormattedData.zipfile)
##############################################################################



def initialize(*args, **keywords):
   
    mows_pygdp = get_module_registry()
    mows_pygdp.add_module(mows_pyGDP)
    
    format_step = get_module_registry()
    format_step.add_module(FormatStep)
    
    #parse = get_module_registry()
    #parse.add_module(Parse)
    
    zipData = get_module_registry()
    zipData.add_module(ZipData)




