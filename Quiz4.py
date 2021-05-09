# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 20:46:30 2021

@author: tchis
"""

# Upload a python file (py) that creates variable buffers using airports shapefile.
# If the value of  the FEATURE field in the airport shapefile is "seaplane" then create a 7,500-meter,
# if the value is "airport" then create a 15,000 meter buffer.  For other values do not create buffers.
# Save the buffers into buffer_airports shapefile. 

def VariableAirportsBuffer(airports):
    
    # Import the required modules
    import arcpy
    import sys
    import traceback
    
    try:
        
        # Name a new field to hold buffer distance values and create it in the airports shapefile
        new_field = 'BUFFER_by_FEATURE'
        arcpy.AddField_management(airports, new_field, 'SHORT')
        
        # Create an update cursor to read the rows of the airports shapefile under the FEATURE field
        with arcpy.da.UpdateCursor(airports,['FEATURE', new_field]) as ap_cursor:
            for row in ap_cursor:
                feature = row[0]
                if feature == 'Seaplane Base':
                    row[1] = 7500 # Set the buffer distance to 7500 for Seaplane Base features
                elif feature == 'Airport':
                    row[1] = 15000 # Set the buffer distance to 15000 for Airport features
                else: pass # Don't create buffer distances for other features
                ap_cursor.updateRow(row) #Update the row
        
        # Run the buffer operation using the new buffer distance field to create buffers for points
        arcpy.Buffer_analysis(airports,'buffer_airports', new_field)
        # Delete the buffer distance field from the airports shapefile now that it is no longer needed 
        arcpy.DeleteField_management(airports, new_field)
    
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