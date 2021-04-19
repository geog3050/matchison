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
# Problem 1 (20 points)
# 
# Given an input point feature class (e.g., facilities or hospitals) and a polyline feature class, i.e., bike_routes:
# Calculate the distance of each facility to the closest bike route and append the value to a new field.
#        
###################################################################### 
def calculateDistanceFromPointsToPolylines(input_geodatabase, fcPoint, fcPolyline):
    # Import the necessary modules
    import arcpy
    import sys
    import traceback
    
    # Set the current workspace
    arcpy.env.workspace = input_geodatabase
    
    # Define custom exceptions
    class gdbEmptyError(Exception):
        pass
    class pointError(Exception):
        pass
    class lineError(Exception):
        pass
    
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
        
        # Test if point feature class shapeType is valid
        desc = arcpy.Describe(fcPoint)
        if desc.shapeType != "Point":
            raise pointError
        else: pass
        
        # Test if polyline feature class shapeType parameter is valid
        desc = arcpy.Describe(fcPolyline)
        if desc.shapeType != "Polyline":
            raise lineError
        else: pass
    
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")

    except pointError:
        print("pointError: shape type is not valid (point feature class).")
    
    except lineError:
        print("lineError: shape type is not valid (polyline feature class).")
    
    else:
        # Calculate the nearest input linear feature to each input point feature;
        # appends linear feature FID to NEAR_FID, and distance (in feet) to NEAR_DIST
        try:
            arcpy.analysis.Near(fcPoint, fcPolyline, search_radius="FEET", method="GEODESIC")
        
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
# Problem 2 (30 points)
# 
# Given an input point feature class, i.e., facilities, with a field name (FACILITY) and a value ('NURSING HOME'), and a polygon feature class, i.e., block_groups:
# Count the number of the given type of point features (NURSING HOME) within each polygon and append the counts as a new field in the polygon feature class.
#
######################################################################
def countPointsByTypeWithinPolygon(input_geodatabase, fcPoint, pointFieldName, pointFieldValue, fcPolygon):
    # Import the necessary modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Set the current workspace
    arcpy.env.workspace = input_geodatabase
    
    # Define custom exceptions
    class gdbEmptyError(Exception):
        pass
    class pointError(Exception):
        pass
    class polygonError(Exception):
        pass
    class fieldsError(Exception):
        pass
    class attributeValueError(Exception):
        pass
    
    
    try:
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(input_geodatabase,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
                
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
        
        # Test if polygon feature class shapeType parameter is valid
        desc = arcpy.Describe(fcPolygon)
        if desc.shapeType != "Polygon":
            raise polygonError
        else: pass
                
        # Test if point feature class shapeType is valid
        desc = arcpy.Describe(fcPoint)
        if desc.shapeType != "Point":
            raise pointError
        else: pass
        
        # Test if pointFieldName exists in fcPoint
        fields = arcpy.ListFields(fcPoint)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if pointFieldName in fieldstest:
            pass
        else: raise fieldsError
            
        # Test if pointFieldValue is present in pointFieldName
        # Search the points layer with a cursor, add distinct values to listval
        listval = []
        with arcpy.da.SearchCursor(fcPoint, pointFieldName) as scursor:
            for row in scursor:
                if row[0] in listval:
                    pass
                else:
                    listval.append(row[0])
        if pointFieldValue in listval:
            pass
        else: raise attributeValueError
    
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")
    
    except pointError:
        print("pointError: shape type is not valid (point feature class).")
    
    except polygonError:
        print("polygonError: shape type is not valid (polygon feature class).")
        
    except fieldsError:
        print("fieldsError: specified field could not be found within the specified point feature class.")
    
    except attributeValueError:
        print("attributeValueError: specified attribute value could not be found within the specified field")

    else: 
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
    
        try:
            # Construct a query using the specified point feature class, field name, and field value
            query = buildWhereClause(fcPoint, pointFieldName, pointFieldValue)
      
            # Select features from the point feature class using the query, and export to a new layer
            arcpy.analysis.Select(fcPoint, "point_select", query)
    
            # Use Summarize Within tool to count selected points within polygons and export to "polygon_temp"
            arcpy.analysis.SummarizeWithin(fcPolygon, "point_select", "polygon_temp", keep_all_polygons = "KEEP_ALL", sum_shape = "ADD_SHAPE_SUM")
    
            # Rename count output field to change from default
            arcpy.management.AlterField("polygon_temp", "Point_Count", "Select_Count", "Select_Count")
    
            # Join the count field to the original polygon input file
            arcpy.management.JoinField(fcPolygon, "OBJECTID", "polygon_temp", "OBJECTID", fields = "Select_Count")
            
            # Join the workspace filepath to the temporary files
            pointpath = os.path.join(input_geodatabase,"point_select")
            polypath = os.path.join(input_geodatabase,"polygon_temp")
    
            # Delete the temporary files that are no longer necessary
            arcpy.management.Delete([pointpath, polypath])
    
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
# Problem 3 (50 points)
# 
# Given a polygon feature class, i.e., block_groups, and a point feature class, i.e., facilities,
# with a field name within point feature class that can distinguish categories of points (i.e., FACILITY);
# count the number of points for every type of point features (NURSING HOME, LIBRARY, HEALTH CENTER, etc.) within each polygon and
# append the counts to a new field with an abbreviation of the feature type (e.g., nursinghome, healthcenter) into the polygon feature class 

# HINT: If you find an easier solution to the problem than the steps below, feel free to implement.
# Below steps are not necessarily explaining all the code parts, but rather a logical workflow for you to get started.
# Therefore, you may have to write more code in between these steps.

# 1- Extract all distinct values of the attribute (e.g., FACILITY) from the point feature class and save it into a list
# 2- Go through the list of values:
#    a) Generate a shortened name for the point type using the value in the list by removing the white spaces and taking the first 13 characters of the values.
#    b) Create a field in polygon feature class using the shortened name of the point type value.
#    c) Perform a spatial join between polygon features and point features using the specific point type value on the attribute (e.g., FACILITY)
#    d) Join the counts back to the original polygon feature class, then calculate the field for the point type with the value of using the join count field.
#    e) Delete uncessary files and the fields that you generated through the process, including the spatial join outputs.  
######################################################################
def countCategoricalPointTypesWithinPolygons(fcPoint, pointFieldName, fcPolygon, workspace):
    
    # Import the necessary modules
    import arcpy
    import os
    import sys
    import traceback
    
    # Set the current workspace
    workspace = arcpy.env.workspace
    
    # Define custom exceptions
    class gdbEmptyError(Exception):
        pass
    class pointError(Exception):
        pass
    class polygonError(Exception):
        pass
    class fieldsError(Exception):
        pass
    
    try:
        # Test if there are any feature classes in the specified folder or geodatabase
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        fclist = []
        checkwalk = arcpy.da.Walk(workspace,datatype = "FeatureClass")
        for dirpath, dirnames, filenames in checkwalk:
            for file in filenames:
                fclist.append(str(file))
                
        # If fclist is empty, then there were no feature classes in the specified folder or geodatabase
        if not fclist:
            raise gdbEmptyError
        else: pass
        
        # Test if polygon feature class shapeType parameter is valid
        desc = arcpy.Describe(fcPolygon)
        if desc.shapeType != "Polygon":
            raise polygonError
        else: pass
                
        # Test if point feature class shapeType is valid
        desc = arcpy.Describe(fcPoint)
        if desc.shapeType != "Point":
            raise pointError
        else: pass
        
        # Test if pointFieldName exists in fcPoint
        fields = arcpy.ListFields(fcPoint)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if pointFieldName in fieldstest:
            pass
        else: raise fieldsError
            
    except gdbEmptyError:
        print("gdbEmptyError: Workspace appears to contain no feature classes, or may not exist.")
    
    except pointError:
        print("pointError: shape type is not valid (point feature class).")
    
    except polygonError:
        print("polygonError: shape type is not valid (polygon feature class).")
        
    except fieldsError:
        print("fieldsError: specified field could not be found within the specified point feature class.")
        
    else:
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
        
        try:
            # Create a list
            listval = []
    
            # Search the points layer with a cursor, add distinct values to listval
            with arcpy.da.SearchCursor(fcPoint, pointFieldName) as scursor:
                for row in scursor:
                    if row[0] in listval:
                        pass
                    else:
                        listval.append(row[0])
                
            # Use listval to generate acceptable field names
            shortval = [i.replace(" ", "")[:13] for i in listval]
            names = [arcpy.ValidateFieldName(i) for i in shortval]
    
            for i in listval:
                # Construct a query using the specified point feature class, field name, and field value
                query = buildWhereClause(fcPoint, pointFieldName, i)
        
                # Record the index position in listval
                ind = listval.index(i)
        
                # Use the index to refer to the abbreviated version of the listval entry in the names list
                name = names[ind]
        
                # Select features from the point feature class using the query, and export to a new layer
                arcpy.analysis.Select(fcPoint, "point_select", query)
        
                # Use Summarize Within tool to count selected points within polygons and export to "polygon_temp"
                arcpy.analysis.SummarizeWithin(fcPolygon, "point_select", "polygon_temp", sum_shape = "ADD_SHAPE_SUM")
        
                # Rename count output field to change from default
                arcpy.management.AlterField("polygon_temp", "Point_Count", name, name)
        
                # Join the count field to the original polygon input file
                arcpy.management.JoinField(fcPolygon, "OBJECTID", "polygon_temp", "OBJECTID", fields = name)
        
                # Join the workspace filepath to the temporary files
                pointpath = os.path.join(workspace, "point_select")
                polypath = os.path.join(workspace, "polygon_temp")
        
                # Delete the temporary files that are no longer necessary
                arcpy.management.Delete([pointpath, polypath])
                
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
