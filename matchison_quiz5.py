# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:33:23 2021

@author: tchis
"""

#QUIZ PROMPT:
    
#Please write a python function that takes three inputs as and achieves the task defined below:

#calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2):

#Given an input polygon feature class, fcPolygonA (e.g., parks), and a second feature class, fcPolygonB (e.g., block_groups) :

#Calculate the percentage of the area of the first polygon features (fcPolygonA ) in the second polygon features (fcPolygonB), and 
#append the percentage of park area into a new field in the block groups feature class
#Make sure that your area calculations are as accurate as possible.


def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPolygon1, fcPolygon2):

    # Import the necessary modules
    import arcpy
    import sys
    import traceback
    
    # Set the current workspace
    arcpy.env.workspace = input_geodatabase
    
    # Define custom exception
    class gdbEmptyError(Exception):
        pass
    
    # Test if there are any feature classes in the specified folder or geodatabase
    try:
        fclist = []
        # Walk through the input folder or geodatabase and find all feature classes; add their names to the fclist
        checkwalk = arcpy.da.Walk(input_geodatabase, datatype = "FeatureClass")
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
        
        # Calculate geodesic area (most accurate) of fcPolygon2 in square kilometers.
        arcpy.AddGeometryAttributes_management(fcPolygon2, "AREA_GEODESIC", "KILOMETERS")
        
        # Find areas where both polygon feature classes overlap.
        poly_inter = "polygons_intersect"
        arcpy.Intersect_analysis([fcPolygon1, fcPolygon2], poly_inter)
        
        # Calculate geodesic area (most accurate) of fcPolygon2 within area of fcPolygon1 in square kilometers.
        arcpy.AddGeometryAttributes_management(poly_inter, "AREA_GEODESIC", "KILOMETERS")
        
        # Create a dictionary
        poly_dict = dict()
        # Search the intersect output layer with a cursor
        with arcpy.da.SearchCursor(poly_inter, ["FIPS", "AREA_GEO"]) as scursor:
            for row in scursor:
                fips = row[0]
                if fips in poly_dict.keys():
                    poly_dict[fips] += row[1] # If an identical id has already been read, add the geodesic area to the area already recorded for that id
                else:
                    poly_dict[fips] = row[1] # If the id has not already been read, create an entry for that id and record the geodesic area
        
        # Create a new field in fcPolygon2 to store the aggregated geodesic areas of the intersect output
        inter_area = "inter_area"
        arcpy.AddField_management(fcPolygon2, inter_area, "DOUBLE")
        
        # Use the update cursor to populate the new field
        with arcpy.da.UpdateCursor(fcPolygon2, ["FIPS", inter_area]) as ucursor:
            for row in ucursor:
                if row[0] in poly_dict.keys():
                    row[1] = poly_dict[row[0]]
                else:
                    row[1] = 0
                ucursor.updateRow(row)
                
        # Create a new field in fcPolygon2 to store the calculated percent value
        inter_pct = "inter_pct"
        arcpy.AddField_management(fcPolygon2, inter_pct, "DOUBLE")
        
        # Populate the percent value field by dividing the intersection output area by the fcPolygon2 area
        arcpy.CalculateField_management(fcPolygon2, inter_pct, "!inter_area!/!AREA_GEO!", "PYTHON3")
    
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