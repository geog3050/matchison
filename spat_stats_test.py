# -*- coding: utf-8 -*-
"""
Created on Sun May  9 02:27:47 2021

@author: tchis
"""

def spatstatstest(report_name, input_fc, resvar, expvar1, expvar2, expvar3, input_geodatabase):
    
    # Import the necessary modules
    import arcpy
    import sys
    import traceback
    
    # Enable overwriting
    arcpy.env.overwriteOutput = True
    
    # Set the current workspace
    arcpy.env.workspace = input_geodatabase
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class WorkspaceEmptyError(Exception):
        pass
    class fcExistsError(Exception):
        pass
    class fieldExistsError(Exception):
        pass
    
    
    try:
        # Test if workspace exists
        if arcpy.Exists(input_geodatabase):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
        
        # Test if there are any feature classes in the specified folder or geodatabase
        fclist = []
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        checkwalk = arcpy.da.Walk(input_geodatabase, datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise WorkspaceEmptyError
        else: pass
    
        # Test if input_fc exists
        if arcpy.Exists(input_fc):
            print("Specified feature class has been found.")
        else:
            raise fcExistsError
            
        # Test if all variables exist as fields in input_fc
        varlist = [resvar, expvar1, expvar2, expvar3]
        fields = arcpy.ListFields(input_fc)
        fieldstest = []
        for var in varlist:
            for f in fields:
                fieldstest.append(f.name)
            if var in fieldstest:
                pass
            else: raise fieldExistsError
            
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace (geodatabase or folder) could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: The workspace (geodatabase or folder) appears to contain no feature classes!")
        
    except fcExistsError:
        print("fcExistsError: The specified feature class could not be found!")
        
    except fieldExistsError:
        print("fieldExistsError: At least one of the specified variables cannot be found as a field in the input feature class (input_fc)!")
    
    else:
        try:
            # Generate HTML reports with Moran's I statistic
            for var in varlist:
                arcpy.stats.SpatialAutocorrelation(input_fc, var, "Generate_Report", "CONTIGUITY_EDGES_CORNERS", "EUCLIDEAN_DISTANCE", "NONE")
                
            # Generate exploratory regression model
            arcpy.stats.ExploratoryRegression(input_fc, resvar, [expvar1, expvar2, expvar3], Output_Report_File = report_name)
            
        
        except arcpy.ExecuteError: 
            # Get the tool error messages 
            msgs = arcpy.GetMessages(2) 
    
            # Return tool error messages for use with a script tool 
            arcpy.AddError(msgs) 
    
            # Print tool error messages for use in Python
            print("Tool Error:", msgs)
    
        except:
            # Get the traceback object
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
    
            # Put error information into a message string
            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + arcpy.GetMessages(2) + "\n"
    
            # Return python error messages for use in script tool or Python window
            arcpy.AddError(pymsg)
            arcpy.AddError(msgs)
    
            # Print Python error messages for use in Python / Python window
            print(pymsg)
            print(msgs)
        
        print("All operations complete!")