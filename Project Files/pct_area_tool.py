# -*- coding: utf-8 -*-
"""
Created on Wed Mar 24 09:33:23 2021

@author: tchis
"""

def calculatePercentAreaOfPolygonAInPolygonB(input_geodatabase, fcPoint, fcPolygon, id_field, out_name):

    # Import the necessary modules
    import arcpy
    import os
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
    class fcPolygonExistsError(Exception):
        pass
    class fcPolygonShapeError(Exception):
        pass
    class fcPointExistsError(Exception):
        pass
    class fcPointShapeError(Exception):
        pass
    class fieldNameError(Exception):
        pass
    class attributeValueError(Exception):
        pass
    class fcCoordSysError(Exception):
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
    
        # Test if fcPolygon exists
        if arcpy.Exists(fcPolygon):
            print("Specified polygon feature class has been found.")
        else:
            raise fcPolygonExistsError
        
        # Test if polygon feature class shapeType parameter is valid
        descpoly = arcpy.Describe(fcPolygon)
        if descpoly.shapeType != "Polygon":
            raise fcPolygonShapeError
        else: print("Specified feature class has the correct shape type for this script (polygon).")
        
        # Test if fcPoint exists
        if arcpy.Exists(fcPoint):
            print("Specified point feature class has been found.")
        else:
            raise fcPointExistsError
        
        # Test if point feature class shapeType parameter is valid
        descpoint = arcpy.Describe(fcPoint)
        if descpoint.shapeType != "Point":
            raise fcPointShapeError
        else: print("Specified feature class has the correct shape type for this script (point).")
        
        # Test if id_field attribute exists in fcPolygon
        fields = arcpy.ListFields(fcPolygon)
        fieldstest = []
        for f in fields:
            fieldstest.append(f.name)
        if id_field in fieldstest:
            print("Specified field has been found in the feature class.")
        else: raise fieldNameError
        
    except WorkspaceExistsError:
        print("WorkspaceExistsError: The specified workspace (geodatabase or folder) could not be found!")
        
    except WorkspaceEmptyError:
        print("WorkspaceEmptyError: The workspace (geodatabase or folder) appears to contain no feature classes!")
        
    except fcPolygonExistsError:
        print("fcPolygonExistsError: The specified polygon feature class could not be found!")
        
    except fcPolygonShapeError:
        print("fcPolygonShapeError: The specified feature class must be a polygon feature class!")
        
    except fcPointExistsError:
        print("fcPointExistsError: The specified point feature class could not be found!")
        
    except fcPointShapeError:
        print("fcPointShapeError: The specified feature class must be a point feature class!")
    
    except fieldNameError:
        print("fieldNameError: The specified attribute field could not be found within the specified feature class!")
    
    # If no exceptions are raised, attempt to carry out the procedure
    else:
        try:
            # Create spatial reference objects for input feature classes
            point_sref = descpoint.spatialReference
            poly_sref = descpoly.spatialReference
            
            # If they match and are both projected coordinate systems, proceed.
            if point_sref.name == poly_sref.name and point_sref.type == "Projected" and poly_sref.type == "Projected":
                inpoly = fcPolygon
                inpoint = fcPoint
                print("Point and Polygon feature class projections match.")
            # If they don't match and:
            else:
                print("Point and Polygon feature class projections do not match!")
                # Are both projected coordinate systems, project the polygon to match the point
                if point_sref.type == "Projected" and poly_sref.type == "Projected":
                    inpoint = fcPoint
                    inpoly = fcPolygon + "_proj"
                    arcpy.management.Project(fcPolygon, inpoly, point_sref)
                    print("Polygon feature class projected to match point feature class.")
                # The point has a geographic coordinate system while the polygon has a projected coordinate system
                elif point_sref.type == "Geographic" and poly_sref.type == "Projected":
                    inpoint = fcPoint + "_proj"
                    inpoly = fcPolygon
                    arcpy.management.Project(fcPoint, inpoint, poly_sref)
                    print("Point feature class projected to match polygon feature class.")
                # The point has a projected coordinate system while the polygon has a geographic coordinate system
                elif point_sref.type == "Projected" and poly_sref.type == "Geographic":
                    inpoint = fcPoint
                    inpoly = fcPolygon + "_proj"
                    arcpy.management.Project(fcPolygon, inpoly, point_sref)
                    print("Polygon feature class projected to match point feature class.")  
                # The point and polygon both have a geographic coordinate system
                elif point_sref.type == "Geographic" and poly_sref.type == "Geographic":
                    raise fcCoordSysError
                    
            # Clarify which polygon file is being used in the script
            print("The script will proceed using the following feature classes: ")
            print("Polygon: ", inpoly)
            print("Point: ", inpoint)
            
            # Buffer the points field
            # Buffer to 1 US mile
            buff1 = fcPoint + "_buff1"
            arcpy.analysis.Buffer(inpoint, buff1, "1 Miles", dissolve_option = "ALL", method = "GEODESIC")
            # Buffer to 3 US miles
            buff3 = fcPoint + "_buff3"
            arcpy.analysis.Buffer(inpoint, buff3, "3 Miles", dissolve_option = "ALL", method = "GEODESIC")
            # Buffer to 5 US miles
            buff5 = fcPoint + "_buff5"
            arcpy.analysis.Buffer(inpoint, buff5, "5 Miles", dissolve_option = "ALL", method = "GEODESIC")
            print("Buffer operation complete.")
            
            # Calculate geodesic area (most accurate) of fcPolygon in square miles.
            arcpy.AddGeometryAttributes_management(inpoly, "AREA_GEODESIC", Area_Unit = "SQUARE_MILES_US")
            
            # Find areas where each buffer and the polygon feature class overlap.
            inter1 = "inter1"
            arcpy.Intersect_analysis([inpoly, buff1], inter1)
            inter3 = "inter3"
            arcpy.Intersect_analysis([inpoly, buff3], inter3)
            inter5 = "inter5"
            arcpy.Intersect_analysis([inpoly, buff5], inter5)
            print("Intersect operation complete.")
            
            
            # Calculate geodesic area (most accurate) of buffers within area of fcPolygon in square miles.
            arcpy.AddGeometryAttributes_management(inter1, "AREA_GEODESIC", Area_Unit = "SQUARE_MILES_US")
            arcpy.AddGeometryAttributes_management(inter3, "AREA_GEODESIC", Area_Unit = "SQUARE_MILES_US")
            arcpy.AddGeometryAttributes_management(inter5, "AREA_GEODESIC", Area_Unit = "SQUARE_MILES_US")
            print("Area of buffer within polygons calculated.")
            
            # Create percentage values for buffer areas within polygons
            inters = [inter1, inter3, inter5]
            for i in inters:
                # Create a dictionary
                poly_dict = dict()
                # Search the intersect output layer with a cursor
                with arcpy.da.SearchCursor(i, [id_field, "AREA_GEO"]) as scursor:
                    for row in scursor:
                        idf = row[0]
                        if idf in poly_dict.keys():
                            poly_dict[idf] += row[1] # If an identical id has already been read, add the geodesic area to the area already recorded for that id
                        else:
                            poly_dict[idf] = row[1] # If the id has not already been read, create an entry for that id and record the geodesic area
            
                # Create a new field in fcPolygon to store the aggregated geodesic areas of the intersect output
                inter_area = "inter_area"
                arcpy.AddField_management(inpoly, inter_area, "DOUBLE")
            
                # Use the update cursor to populate the new field
                with arcpy.da.UpdateCursor(inpoly, [id_field, inter_area]) as ucursor:
                    for row in ucursor:
                        if row[0] in poly_dict.keys():
                            row[1] = poly_dict[row[0]]
                        else:
                            row[1] = 0
                        ucursor.updateRow(row)
                    
                # Create a new field in fcPolygon to store the calculated percent value
                inter_pct = i + "pct"
                arcpy.AddField_management(inpoly, inter_pct, "DOUBLE")
            
                # Populate the percent value field by dividing the intersection output area by the fcPolygon area
                arcpy.CalculateField_management(inpoly, inter_pct, "!inter_area!/!AREA_GEO!*100", "PYTHON3")
                print(inter_pct, " has been added to ", inpoly)
            
            # Delete the inter_area field now that it is no longer needed
            arcpy.management.DeleteField(inpoly, inter_area)
            
            # Rename the output feature class
            arcpy.management.Rename(inpoly, out_name)
                
            # Delete the temporary files now that they are no longer needed
            del1 = os.path.join(input_geodatabase, buff1)
            del2 = os.path.join(input_geodatabase, buff3)
            del3 = os.path.join(input_geodatabase, buff5)
            del4 = os.path.join(input_geodatabase, inter1)
            del5 = os.path.join(input_geodatabase, inter3)
            del6 = os.path.join(input_geodatabase, inter5)
            arcpy.management.Delete([del1, del2, del3, del4, del5, del6])
            print("Unneeded fields and feature classes deleted.")
                
        # Coordinate system exception handling
        except fcCoordSysError:
            print("Both inputs use a geographic coordinate system! Please project at least one input into a suitable projected coordinate system!")
    
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