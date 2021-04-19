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
# Problem 1 (30 Points)
#
# Given a polygon feature class in a geodatabase, a count attribute of the feature class(e.g., population, disease count):
# this function calculates and appends a new density column to the input feature class in a geodatabase.

# Given any polygon feature class in the geodatabase and a count variable:
# - Calculate the area of each polygon in square miles and append to a new column
# - Create a field (e.g., density_sqm) and calculate the density of the selected count variable
#   using the area of each polygon and its count variable(e.g., population) 
# 
# 1- Check whether the input variables are correct(e.g., the shape type, attribute name)
# 2- Make sure overwrite is enabled if the field name already exists.
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate area calculation and conversion
# 4- Give a warning message if the projection is a geographic projection(e.g., WGS84, NAD83).
#    Remember that area calculations are not accurate in geographic coordinate systems. 
# 
###################################################################### 
def calculateDensity(fcpolygon, attribute, geodatabase = "assignment2.gdb"):
    
    # Import the necessary modules
    import arcpy
    import sys
    import traceback
    
    # Enable overwrite
    arcpy.env.overwriteOutput = True
    
    # Set the current workspace
    arcpy.env.workspace = geodatabase
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class WorkspaceEmptyError(Exception):
        pass
    class fcPolygonExistsError(Exception):
        pass
    class fcPolygonShapeError(Exception):
        pass
    class fieldNameError(Exception):
        pass
    class fieldDataTypeError(Exception):
        pass
    class fcCoordSysError(Exception):
        pass
    
    # Check that all specified files exist and parameters are valid
    try:
        # Test if workspace exists
        if arcpy.Exists(geodatabase):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
        
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(geodatabase,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise WorkspaceEmptyError
        else: print("Workspace is not empty.")
    
        # Test if fcpolygon exists
        if arcpy.Exists(fcpolygon):
            print("Specified feature class has been found.")
        else:
            raise fcPolygonExistsError
        
        # Test if polygon feature class shapeType parameter is valid
        descfc = arcpy.Describe(fcpolygon)
        if descfc.shapeType != "Polygon":
            raise fcPolygonShapeError
        else: print("Specified feature class has the correct shape type for this script (polygon).")
        
        # Test if feature class uses a geographic or projected coordinate system
        spatial_ref = descfc.spatialReference
        if spatial_ref.type == "Projected":
            print("Specified feature class uses a projected coordinate system.")
        elif spatial_ref.type == "Geographic":
            raise fcCoordSysError
        
        # Test if attribute exists in fcpolygon
        fields = arcpy.ListFields(fcpolygon)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if attribute in fieldstest:
            print("Specified field has been found in the feature class.")
        else: raise fieldNameError
        
        # Test if attribute data type is appropriate
        attinfo = arcpy.ListFields(fcpolygon, attribute)[0]
        if attinfo.type == "SmallInteger" or attinfo.type == "Integer":
            print("Attribute data type is appropriate for this script.")
        elif attinfo.type == "Single" or attinfo.type == "Double":
            print("WARNING: Data type is numerical, but not an integer! Script will proceed, but please ensure that specified field is count data.")
        else: raise fieldDataTypeError
        
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace (geodatabase or folder) could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: The workspace (geodatabase or folder) appears to contain no feature classes!")
        
    except fcPolygonExistsError:
        print("fcPolygonExistsError: The specified polygon feature class could not be found!")
        
    except fcPolygonShapeError:
        print("fcPolygonShapeError: The specified feature class must be a polygon feature class!")
        
    except fcCoordSysError:
        print("fcCoordSysError: Specified feature class uses a geographic coordinate system! Area calculations are likely to be inaccurate, and the linear distance unit cannot be obtained.")
    
    except fieldNameError:
        print("fieldNameError: The specified attribute field could not be found within the specified feature class!")
    
    except fieldDataTypeError:
        print("fieldDataTypeError: The attribute field must have a numeric data type!")
    
    # If no exceptions are raised, attempt to carry out the procedure
    else:
        try:
            # Identify the input coordinate systems unit of measurement
            print("The linear unit of measurement for the area calculations is: ", spatial_ref.linearUnitName)
            
            # Calculate the geodesic area (units specified in spatial reference used by default) in a new field
            arcpy.management.AddGeometryAttributes(fcpolygon, "AREA_GEODESIC")
            
            # Add new density field and populate by dividing the attribute field by the geodesic area
            arcpy.management.CalculateField(fcpolygon, "density_sq_u", "!{}!/!AREA_GEO!".format(attribute))
        
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
# Problem 2 (40 Points)
# 
# Given a line feature class (e.g.,river_network.shp) and a polygon feature class (e.g.,states.shp) in a geodatabase, 
# id or name field that could uniquely identify a feature in the polygon feature class
# and the value of the id field to select a polygon (e.g., Iowa) for using as a clip feature:
# this function clips the linear feature class by the selected polygon boundary,
# and then calculates and returns the total length of the line features (e.g., rivers) in miles for the selected polygon.
# 
# 1- Check whether the input variables are correct (e.g., the shape types and the name or id of the selected polygon)
# 2- Transform the projection of one to other if the line and polygon shapefiles have different projections
# 3- Identify the input coordinate systems unit of measurement (e.g., meters, feet) for an accurate distance calculation and conversion
#        
###################################################################### 
def estimateTotalLineLengthInPolygons(fcLine, fcClipPolygon, polygonIDFieldName, clipPolygonID, geodatabase = "assignment2.gdb"):
    
    # Import the necessary modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Enable overwrite
    arcpy.env.overwriteOutput = True
    
    # Set the current workspace
    arcpy.env.workspace = geodatabase
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class WorkspaceEmptyError(Exception):
        pass
    class fcPolygonExistsError(Exception):
        pass
    class fcPolygonShapeError(Exception):
        pass
    class fcPolylineExistsError(Exception):
        pass
    class fcPolylineShapeError(Exception):
        pass
    class fieldNameError(Exception):
        pass
    class attributeValueError(Exception):
        pass
    
    # Check that all specified files exist and parameters are valid
    try:
        # Test if workspace exists
        if arcpy.Exists(geodatabase):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
        
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(geodatabase,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise WorkspaceEmptyError
        else: print("Workspace is not empty.")
    
        # Test if fcpolygon exists
        if arcpy.Exists(fcClipPolygon):
            print("Specified polygon feature class has been found.")
        else:
            raise fcPolygonExistsError
        
        # Test if polygon feature class shapeType parameter is valid
        descpoly = arcpy.Describe(fcClipPolygon)
        if descpoly.shapeType != "Polygon":
            raise fcPolygonShapeError
        else: print("Specified feature class has the correct shape type for this script (polygon).")
        
        # Test if fcLine exists
        if arcpy.Exists(fcLine):
            print("Specified polyline feature class has been found.")
        else:
            raise fcPolylineExistsError
        
        # Test if polygon feature class shapeType parameter is valid
        descline = arcpy.Describe(fcLine)
        if descline.shapeType != "Polyline":
            raise fcPolylineShapeError
        else: print("Specified feature class has the correct shape type for this script (polyline).")
        
        # Test if attribute exists in fcpolygon
        fields = arcpy.ListFields(fcClipPolygon)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if polygonIDFieldName in fieldstest:
            print("Specified field has been found in the feature class.")
        else: raise fieldNameError
        
        # Test if clipPolygonID is a valid value within polygonIDFieldName
        # Search the feature class with a cursor, add distinct values to listval
        listval = []
        with arcpy.da.SearchCursor(fcClipPolygon, polygonIDFieldName) as cursor:
            for row in cursor:
                if row[0] in listval:
                    pass
                else:
                    listval.append(row[0])
        if clipPolygonID in listval:
            print("Specified value has been found within the specified field.")
        else: raise attributeValueError
        
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace (geodatabase or folder) could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: The workspace (geodatabase or folder) appears to contain no feature classes!")
        
    except fcPolygonExistsError:
        print("fcPolygonExistsError: The specified polygon feature class could not be found!")
        
    except fcPolygonShapeError:
        print("fcPolygonShapeError: The specified feature class must be a polygon feature class!")
        
    except fcPolylineExistsError:
        print("fcPolylineExistsError: The specified polyline feature class could not be found!")
        
    except fcPolylineShapeError:
        print("fcPolylineShapeError: The specified feature class must be a polyline feature class!")
    
    except fieldNameError:
        print("fieldNameError: The specified attribute field could not be found within the specified feature class!")
        
    except attributeValueError:
        print("attributeValueError: specified attribute value could not be found within the specified field!")
    
    # If no exceptions are raised, attempt to carry out the procedure
    else:
        try:
            # Create spatial reference objects for input feature classes
            line_sref = descline.spatialReference
            poly_sref = descpoly.spatialReference
            
            # If they match, proceed.
            if line_sref.name == poly_sref.name:
                inpoly = fcClipPolygon
                print("Line and Polygon feature class projections match.")
            # If they don't match, project the polygon class to match the line class spatial reference
            else:
                inpoly = fcClipPolygon + "_proj"
                arcpy.management.Project(fcClipPolygon, inpoly, line_sref)
                print("Line and Polygon feature class projections do not match.")
            # Clarify which polygon file is being used in the script
            print("The script will proceed using the following polygon feature class: ", inpoly)
            
            # # Identify the input coordinate systems unit of measurement
            # print("The linear unit of measurement for the calculations is: ", line_sref.linearUnitName)
            
            # Define a function to construct a query using entered parameters
            def buildWhereClause(table, field, value):
            
                # Add DBMS-specific field delimiters
                fieldDelimited = arcpy.AddFieldDelimiters(table, field)
            
                # Determine field type
                fieldType = arcpy.ListFields(table, field)[0].type
            
                # Add single-quotes for string field values
                if str(fieldType) == 'String':
                    value = "'%s'" % value
            
                # Format WHERE clause
                whereClause = "%s = %s" % (fieldDelimited, value)
                return whereClause
            
            # Create where clause
            where_clause = buildWhereClause(inpoly, polygonIDFieldName, clipPolygonID)
            
            # Create a temporary file from selected features using the where clause
            arcpy.analysis.Select(inpoly, "polygon_select_temp", where_clause)
            
            # Naming convention for the output file
            output_fc = fcLine + "_clipped"
            
            # Clip the fcLine feature class using the temporary polygon feature class
            arcpy.analysis.Clip(fcLine, "polygon_select_temp", output_fc)
            
            # Calculate the geodesic area (units specified in spatial reference used by default) in a new field
            arcpy.management.AddGeometryAttributes(output_fc, "LENGTH_GEODESIC", "MILES_US")
            
            # Create an empty list and populate it with values from the LENGTH_GEO field using a search cursor
            lenlist = []
            with arcpy.da.SearchCursor(output_fc, "LENGTH_GEO") as scursor:
                for row in scursor:
                    lenlist.append(row[0])
                    
            # Delete the temporary polygon selection file
            polypath = os.path.join(geodatabase, "polygon_select_temp")
            arcpy.management.Delete(polypath)
                    
            # Print the sum of the geodesic lengths in the feature class using lenlist
            print("The total length of the line features within the selected polygon area is {} miles.".format(sum(lenlist)))
            
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
# Problem 3 (30 points)
# 
# Given an input point feature class, (i.e., eu_cities.shp) and a distance threshold and unit:
# Calculate the number of points within the distance threshold from each point (e.g., city),
# and append the count to a new field (attribute).
#
# 1- Identify the input coordinate systems unit of measurement (e.g., meters, feet, degrees) for an accurate distance calculation and conversion
# 2- If the coordinate system is geographic (latitude and longitude degrees) then calculate bearing (great circle) distance
#
######################################################################
def countObservationsWithinDistance(fcPoint, distance, distanceUnit, geodatabase = "assignment2.gdb"):
    
    # Import the necessary modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Enable overwrite
    arcpy.env.overwriteOutput = True
    
    # Set the current workspace
    arcpy.env.workspace = geodatabase
    
    # Define custom exceptions
    class WorkspaceExistsError(Exception):
        pass
    class WorkspaceEmptyError(Exception):
        pass
    class fcPointExistsError(Exception):
        pass
    class fcPointShapeError(Exception):
        pass
    class distValidError(Exception):
        pass
    class distUnitValidError(Exception):
        pass
    
    # Check that all specified files exist and parameters are valid
    try:
        # Test if workspace exists
        if arcpy.Exists(geodatabase):
            print("Specified workspace has been found.")
        else:
            raise WorkspaceExistsError
        
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(geodatabase,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise WorkspaceEmptyError
        else: print("Workspace is not empty.")
    
        # Test if fcpolygon exists
        if arcpy.Exists(fcPoint):
            print("Specified feature class has been found.")
        else:
            raise fcPointExistsError
        
        # Test if polygon feature class shapeType parameter is valid
        descpoint = arcpy.Describe(fcPoint)
        if descpoint.shapeType != "Point":
            raise fcPointShapeError
        else: print("Specified feature class has the correct shape type for this script (point).")
        
        # # Test if feature class uses a geographic or projected coordinate system
        # spatial_ref = descfc.spatialReference
        # if spatial_ref.type == "Projected":
        #     print("Specified feature class uses a projected coordinate system.")
        # elif spatial_ref.type == "Geographic":
        #     raise fcCoordSysError
        
        # Test if distance parameter is valid
        if type(distance) == int or type(distance) == float:
            print("Distance parameter data type is valid.")
        else:
            raise distValidError
            
        # Test if the distance unit parameter is valid
        if type(distanceUnit) == str:
            print("Distance unit parameter data type is valid.")
        else:
            raise distUnitValidError
            
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace (geodatabase or folder) could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: The workspace (geodatabase or folder) appears to contain no feature classes!")
        
    except fcPointExistsError:
        print("fcPointExistsError: The specified point feature class could not be found!")
        
    except fcPointShapeError:
        print("fcPointShapeError: The specified feature class must be a point feature class!")
    
    except distValidError:
        print("distValidError: The specified distance value must be entered as an integer!")
        
    except distUnitValidError:
        print("distUnitValidError: The specified distance unit value must be entered as a string!")
        
    else:
        try:
            # # Identify the input coordinate systems unit of measurement
            # sref = descpoint.spatialReference
            # print("The linear unit of measurement for the calculations is: ", sref.linearUnitName)
            
            # Format search_radius parameter
            search = str(distance) + " " + distanceUnit
            
            # Perform the spatial join to count points in search radius and export to temporary point file
            arcpy.analysis.SpatialJoin(fcPoint, fcPoint, "temp", match_option = "WITHIN_A_DISTANCE_GEODESIC", search_radius = search)
            
            # Join the count attribute field in the temporary feature class back to the original point feature class
            desctemp = arcpy.Describe("temp")
            arcpy.management.JoinField(fcPoint, descpoint.OIDFieldName, "temp", desctemp.OIDFieldName, "Join_Count")
            
            # Delete the temporary file now that it is no longer needed
            temppath = os.path.join(geodatabase, "temp")
            arcpy.management.Delete(temppath)
            
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
    print('### Otherwise, the Autograder will assign 0 points.')
