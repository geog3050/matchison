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
# Problem 1: 20 Points
#
# Given a csv file import it into the database passed as in the second parameter
# Each parameter is described below:

# csvFile: The absolute path of the file should be included (e.g., C:/users/ckoylu/test.csv)
# geodatabase: The workspace geodatabase
###################################################################### 
def importCSVIntoGeodatabase(csvFile, geodatabase):
    
    # Import necessary modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Allow overwriting
    arcpy.env.overwriteOutput = True
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class inTableExistsError(Exception):
        pass
    
    # Check that all specified files exist and parameters are valid
    try:
        # Test if workspace exists
        if arcpy.Exists(geodatabase):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
            
        # Test if inTable exists
        if arcpy.Exists(csvFile):
            print("Specified table has been found.")
        else:
            raise inTableExistsError
    
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace could not be found!")
    except inTableExistsError:
        print("inTableExistsError: The specified table could not be found!")
    
    # If no exceptions are raised, attempt to carry out the procedure
    else:
        try:      
            # Create output table name using the 
            basename = os.path.basename(csvFile)
            outTable = os.path.splitext(basename)[0]
            
            # Set the appropriate field delimiters for the data type
            expression = arcpy.AddFieldDelimiters(arcpy.env.workspace, "stationID") + " <> 'IA0000'"
            
            # Execute TableToTable
            arcpy.TableToTable_conversion(csvFile, geodatabase, outTable, expression)
            
        # Catch-all exception handling
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
        
        else:
            print("All script operations now complete!")

##################################################################################################### 
# Problem 2: 80 Points Total
#
# Given a csv table with point coordinates, this function should create an interpolated
# raster surface, clip it by a polygon shapefile boundary, and generate an isarithmic map

# You can organize your code using multiple functions. For example,
# you can first do the interpolation, then clip then equal interval classification
# to generate an isarithmic map

# Each parameter is described below:

# inTable: The name of the table that contain point observations for interpolation       
# valueField: The name of the field to be used in interpolation
# xField: The field that contains the longitude values
# yField: The field that contains the latitude values
# inClipFc: The input feature class for clipping the interpolated raster
# workspace: The geodatabase workspace

# Below are suggested steps for your program. More code may be needed for exception handling
#    and checking the accuracy of the input values.

# 1- Do not hardcode any parameters or filenames in your code.
#    Name your parameters and output files based on inputs. For example,
#    interpolated raster can be named after the field value field name 
# 2- You can assume the input table should have the coordinates in latitude and longitude (WGS84)
# 3- Generate an input feature later using inTable
# 4- Convert the projection of the input feature layer
#    to match the coordinate system of the clip feature class. Do not clip the features yet.
# 5- Check and enable the spatial analyst extension for kriging
# 6- Use KrigingModelOrdinary function and interpolate the projected feature class
#    that was created from the point feature layer.
# 7- Clip the interpolated kriging raster, and delete the original kriging result
#    after successful clipping. 
#################################################################################################################### 
def krigingFromPointCSV(inTable, valueField, xField, yField, inClipFc, workspace = "assignment3.gdb"):
    # Import necessary modules
    import arcpy
    import arcpy.sa as sa
    import os
    import sys
    import traceback
    
    # Allow overwriting
    arcpy.env.overwriteOutput = True
    
    # Set workspace environment
    arcpy.env.workspace = workspace
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class inTableExistsError(Exception):
        pass
    class valueFieldExistsError(Exception):
        pass
    class xFieldExistsError(Exception):
        pass
    class yFieldExistsError(Exception):
        pass
    class inClipFcExistsError(Exception):
        pass
    class inClipFcShapeError(Exception):
        pass
    class LicenseError(Exception):
        pass

    # Check that all specified files exist and parameters are valid
    try:
        # Test if workspace exists
        if arcpy.Exists(workspace):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
            
        # Test if inTable exists
        if arcpy.Exists(inTable):
            print("Specified table has been found.")
        else:
            raise inTableExistsError
            
        # Test if valueField, xField, and yField exist in inTable
        fields = arcpy.ListFields(inTable)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if valueField in fieldstest:
            print("Specified value field has been found in the table.")
        else: raise valueFieldExistsError
        if xField in fieldstest:
            print("Specified x field has been found in the table.")
        else: raise xFieldExistsError
        if yField in fieldstest:
            print("Specified y field has been found in the table.")
        else: raise yFieldExistsError
        
        # Test if inClipFc exists
        if arcpy.Exists(inClipFc):
            print("Specified feature class has been found.")
        else:
            raise inClipFcExistsError
            
        # Test if polygon feature class shapeType parameter is valid
        descclip = arcpy.Describe(inClipFc)
        if descclip.shapeType != "Polygon":
            raise inClipFcShapeError
        else: print("Specified feature class has the correct shape type for this script (polygon).")
        
        # Check for Spatial Analyst license
        if arcpy.CheckExtension("Spatial") == "Available":
            arcpy.CheckOutExtension("Spatial")
            print("Spatial Analyst license recognized.")
        else:
            raise LicenseError
    
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace could not be found!")
    except inTableExistsError:
        print("inTableExistsError: The specified table could not be found!")
    except valueFieldExistsError:
        print("valueFieldExistsError: The specified value field could not be found!")
    except xFieldExistsError:
        print("xFieldExistsError: The specified x field could not be found!")
    except yFieldExistsError:
        print("yFieldExistsError: The specified y field could not be found!")
    except inClipFcExistsError:
        print("inClipFcExistsError: The specified feature class could not be found!")
    except inClipFcShapeError:
        print("inClipFcShapeError: The specified feature class must be a polygon shape type!")
    except LicenseError:
        print("LicenseError: Spatial Analyst license is unavailable!")
    
    # If no exceptions are raised, attempt to carry out the procedure
    else:
        try:        
            # Generate an input feature layer using inTable
            points = inTable + "_points"
            arcpy.management.XYTableToPoint(inTable, points, xField, yField)
            print("Point layer created.")
            
            # Create spatial reference object for inClipFc
            spatial_ref = descclip.spatialReference
            
            # Project the points feature layer to the system used by inClipFc
            prjpoints = inTable + "_prjpoints"
            arcpy.management.Project(points, prjpoints, spatial_ref)
            print("Point layer projected to match input polygon feature class.")
            
            # Create a cellSize variable based on the extent
            descpoints = arcpy.Describe(prjpoints)
            cellSize = 0
            width = descpoints.extent.width
            height = descpoints.extent.height
            if width < height:
                cellSize = width / 1000
            else:
                cellSize = height / 1000
            
            # Naming convention for kriging output
            kname = valueField + "_K"
            
            # Interpolate raster surface from points using kriging and save the output
            outKriging = sa.Kriging(prjpoints, valueField, '#', cellSize)
            outKriging.save(kname)
            print("Points interpolated to create raster.")
            
            # Define bounding box rectangle
            rectangle = str(descclip.extent.XMin) + " " + str(descclip.extent.YMin) + " " + str(descclip.extent.XMax) + " " + str(descclip.extent.YMax)
            
            # Naming convention for clipped kriging output
            cname = kname + "_C"
            
            # Clip the kriging output using the defined feature class
            arcpy.Clip_management(kname, rectangle, cname, inClipFc, "#", "ClippingGeometry", "MAINTAIN_EXTENT")
            print("Raster layer clipped.")
            
            # Naming convention for integerized raster
            iname = cname + "_I"
            
            # Truncate raster cell values to integers and save the output
            outInt = sa.Int(cname)
            outInt.save(iname)
            print("Clipped raster layer values truncated to integers.")
            
            # Get minimum and maximum cell values
            min_F2018 = arcpy.management.GetRasterProperties(outInt, "MINIMUM")
            max_F2018 = arcpy.management.GetRasterProperties(outInt, "MAXIMUM")
            min_2018 = int(min_F2018.getOutput(0)) 
            max_2018 = int(max_F2018.getOutput(0)) 
            
            # Define the number of classes to use
            numofclasses = 5
            
            # Use number of classes and min and max values to calculate equal intervals
            eq_interval = (max_2018 - min_2018) / numofclasses
            
            # Create classification scheme
            remapRangeList = []
            mybreak = min_2018
            for i in range(0, numofclasses):
                newClassCode = i + 1
                lowerBound = int(mybreak)
                upperBound = int(mybreak + eq_interval)
                remap = [lowerBound, upperBound, newClassCode]
                remapRangeList.append(remap)
                mybreak += eq_interval    
            
            # Reclassify the raster
            rname = iname + "_R"
            outReclassRR = sa.Reclassify(iname, "Value", sa.RemapRange(remapRangeList), "NODATA")
            outReclassRR.save(rname)
            print("Raster values reclassified.")
            
            # Convert the raster into a polygon feature class
            arcpy.RasterToPolygon_conversion(rname, valueField + "_ismc")
            print("Raster converted to vector (polygon feature class).")
            
            # Delete unnecessary intermediate stages
            del1 = os.path.join(workspace, points)
            del2 = os.path.join(workspace, prjpoints)
            del3 = os.path.join(workspace, kname)
            del4 = os.path.join(workspace, cname)
            del5 = os.path.join(workspace, iname)
            del6 = os.path.join(workspace, rname)
            arcpy.management.Delete([del1,del2,del3,del4,del5,del6])
            print("Unnecessary files deleted.")
        
        # Catch-all exception handling
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
        
        else:
            print("All script operations now complete!")
    
######################################################################
# MAKE NO CHANGES BEYOND THIS POINT.
######################################################################
if __name__ == '__main__' and hawkid()[1] == "hawkid":
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
