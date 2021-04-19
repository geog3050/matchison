###################################################################### 
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
# 
# Note: Your hawkid is the login name you use to access ICON, and not
# your firsname-lastname@uiowa.edu email address.
# 
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
###################################################################### 
def hawkid():
    return(["Michael Aitchison", "matchison"])

###################################################################### 
# Problem 1 (10 Points)
#
# This function reads all the feature classes in a workspace (folder or geodatabase) and
# prints the name of each feature class and the geometry type of that feature class in the following format:
# 'states is a point feature class'

###################################################################### 
def printFeatureClassNames(workspace):
    
    # Import necessary modules
    import arcpy
    import os
    import sys
    import traceback
       
    # Define custome exception
    class gdbEmptyError(Exception):
        pass
    
    # Test if there are any feature classes in the specified folder or geodatabase
    try:
        fclist = []
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        checkwalk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
                
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")            
                
    try:
        # Walk through the input folder or geodatabase and find all feature classes
        walk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in walk:
            for file in filenames:
                fclist.append(str(file))
                infc = os.path.join(dirpath,file)
                # Describe each feature classes, and print a sentence with its name and shapeType
                desc = arcpy.Describe(infc)
                print("{0} is a {1} feature class"
                      .format(desc.name, desc.shapeType))
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

###################################################################### 
# Problem 2 (20 Points)
#
# This function reads all the attribute names in a feature class or shape file and
# prints the name of each attribute name and its type (e.g., integer, float, double)
# only if it is a numerical type

###################################################################### 
def printNumericalFieldNames(inputFc, workspace):
    
    # Import necessary modules
    import arcpy
    import sys
    import traceback
    
    # Define custome exception
    class gdbEmptyError(Exception):
        pass
    
    # Test if there are any feature classes in the specified folder or geodatabase
    try:
        fclist = []
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        checkwalk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
                
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")
    
    try:
        # Set the current workspace
        arcpy.env.workspace = workspace
        # List the fields in the specified feature class, and for each one if it has a numerical data type print a sentence with its name and data type; otherwise ignore it
        fields = arcpy.ListFields(inputFc)
        for f in fields:
            if f.type == "Integer" or f.type == "SmallInteger" \
                or f.type == "Single" or f.type == "Double":
                print("{0} has the numerical data type {1}"
                      .format(f.name, f.type))
            else: pass
    
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
    

###################################################################### 
# Problem 3 (30 Points)
#
# Given a geodatabase with feature classes, and shape type (point, line or polygon) and an output geodatabase:
# this function creates a new geodatabase and copying only the feature classes with the given shape type into the new geodatabase

###################################################################### 
def exportFeatureClassesByShapeType(input_geodatabase, shapeType, output_geodatabase):
    
    # Import necessary modules
    import arcpy
    import sys
    import os
    import traceback
    
    # Define custome exceptions
    class shapeTypeError(Exception):
        pass
    class gdbEmptyError(Exception):
        pass
    
    # Test if shapeType parameter is valid (i.e. not misspelled or incorrectly capitalized)
    try:
        if shapeType != "Point" and shapeType != "Polyline" and shapeType != "Polygon":
            raise shapeTypeError
        else: pass
    except shapeTypeError:
        print("shapeTypeError: shapeType parameter is not valid. Check spelling and capitalization (first letter should be capitalized).")
    
    # Test if there are any feature classes in the specified folder or geodatabase
    try:
        fclist = []
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        checkwalk = arcpy.da.Walk(input_geodatabase,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
    
    except gdbEmptyError:
        print("gdbEmptyError: Input geodatabase or folder appears to contain no feature classes, or may not exist.")

            
    try:
        # Set the filepath for output_geodatabase to be the same as for the input, so that the copy will be in the same directory
        outpath = os.path.dirname(os.path.abspath(input_geodatabase))
        outgdb = str(arcpy.CreateFileGDB_management(outpath, output_geodatabase))
        
        # Walk through the input folder or geodatabase and find all feature classes
        walk = arcpy.da.Walk(input_geodatabase, datatype = "FeatureClass")
        for dirpath, dirnames, filenames in walk:
            for file in filenames:
                infc = os.path.join(dirpath,file)
                # Describe the feature classes, and if the described shapetype matches the user specification, copy it to the new output geodatabase; otherwise ignore it
                desc = arcpy.Describe(infc)
                if desc.shapeType == shapeType:
                    outfc = os.path.join(outgdb,desc.baseName)
                    arcpy.CopyFeatures_management(infc,outfc)
                else: pass
                    
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

###################################################################### 
# Problem 4 (40 Points)
#
# Given an input feature class or a shape file and a table in a geodatabase or a folder workspace,
# join the table to the feature class using one-to-one and export to a new feature class.
# Print the results of the joined output to show how many records matched and unmatched in the join operation. 

###################################################################### 
def exportAttributeJoin(inputFc, idFieldInputFc, inputTable, idFieldTable, workspace):

    # Import necessary modules
    import arcpy
    import sys
    import traceback
    
    # Define custome exception
    class gdbEmptyError(Exception):
        pass
    
    # Test if there are any feature classes in the specified folder or geodatabase
    try:
        fclist = []
        checkwalk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
    
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")

    try:
        # Set the current workspace 
        arcpy.env.workspace = workspace

        # Naming convention for output feature class
        outputFc = inputFc + "_joinexport"

        # Test the join between the specified feature layer and table
        val_res = arcpy.ValidateJoin_management(inputFc, idFieldInputFc, inputTable, idFieldTable)
        matched = int(val_res[1])
        row_count = int(val_res[2])

        # Validate the join returns matched rows before proceeding
        if matched >= 1:
            arcpy.CopyFeatures_management(inputFc, outputFc)
            arcpy.AddJoin_management(outputFc, idFieldInputFc, inputTable, idFieldTable)
            print(f"Output Features: {outputFc} had {matched} matches and {row_count - matched} unmatched records, and created {row_count} records in total.")
        else: print("The table could not be joined. No new feature classes were created. Make sure that the fields chosen for the feature class and the table have matching records and data types.")
            
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

######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
