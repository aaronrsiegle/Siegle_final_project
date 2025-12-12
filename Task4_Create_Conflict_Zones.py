# Name: Task4_Create_Conflict_Zones 
# Date: 12/8/2025
# Description: This script finds the areas where the extracted ICLUS classes and the extracted marsh migration classes overlap for a given year and sea level rise value

#%% Import system modules 
import arcpy
import geopandas as gpd 
import pandas as pd 
import os
import glob

#%% Set workspace 
arcpy.env.workspace = "..\\Scratch"

# Define folders
marsh_data = "..\\Data\\Processed\\Marsh_Migration"
dev_data = "..\\Data\\Processed\\Development_Classes"
output_data = "..\\Data\\Processed\\Conflict_Zones"
inter_data = "..\\Scratch"

#%% Load processed marsh files into a dictionary
# Create dictionary 
marsh_zones = {}

# Select all the marsh files 
tif_files = glob.glob(os.path.join(marsh_data, '*.tif'))

# Add the files to the dictionary 
for tif_file in tif_files: 
     # Extract the filename to use as key 
    filename = os.path.basename(tif_file)
    key = os.path.splitext(filename)[0]  
    marsh_zones[key] = tif_file

# Print the dictionary 
print("\n--- Marsh Files Loaded ---")
print(f"Number of files: {len(marsh_zones)}")
print("\nDictionary contents:")
for key, value in marsh_zones.items():
    print(f"  {key}: {value}")

#%% Load processed development files into a dictionary
# Create dictionary 
dev_zones = {}

# Select all the development files 
dev_files = glob.glob(os.path.join(dev_data, '*.tif'))

# Add the files to the dictionary
for dev_file in dev_files: 
    # Extract the filename to use as key 
    filename_dev = os.path.basename(dev_file)
    key = os.path.splitext(filename_dev)[0]
    dev_zones[key] = dev_file

# Print the dictionary 
print("\n--- Development Files Loaded ---")
print(f"Number of files: {len(dev_zones)}")
print("\nDictionary contents:")
for key, value in dev_zones.items():
    print(f"  {key}: {value}")
#%% Add in User Defined Functions  (UDFs)
SLR_value = arcpy.GetParameterAsText(0)
Year = arcpy.GetParameterAsText(1)

# Convert to float and format with one decimal place
SLR_value_float = float(SLR_value)
SLR_value = f"{SLR_value_float:.1f}"

print ("Sea Level Rise value is {} feet".format(SLR_value))
print ("Year of Development Projection is {}".format(Year))

#%% Select marsh files based on UDFs 
slr_formatted = SLR_value.replace('.', '_')
# Creating list so that multiple files can be selected 
selected_marsh_files = []

# Looping through dictionary to find matching files 
for key, filepath in marsh_zones.items():
    if f"SLR_{slr_formatted}ft" in key:
        selected_marsh_files.append(filepath)
        arcpy.AddMessage(f"Found: {key}")

# Print statements 
if selected_marsh_files:
    arcpy.AddMessage(f"\n--- Selected Marsh File ---")
    arcpy.AddMessage(f"Found {len(selected_marsh_files)} files for SLR value {SLR_value} feet:")
    for filepath in selected_marsh_files:
        arcpy.AddMessage(f"  {filepath}")
else:
    arcpy.AddError(f"No marsh file found for SLR value {SLR_value} feet")

#%% Select development files based on UDFs 
# Creatign list 
selected_dev_files = []

# Looping through dictionary to find matching files 
for key, filepath in dev_zones.items(): 
    if f"ICLUS_{Year}_processed" in key: 
        selected_dev_files.append(filepath)
        arcpy.AddMessage(f"Found: {key}")

# Print statement 
if selected_dev_files:
    arcpy.AddMessage(f"\n--- Selected Development File ---")
    arcpy.AddMessage(f"Found {len(selected_dev_files)} files for the year {Year}:")
    for filepath in selected_dev_files:
       arcpy.AddMessage(f"  {filepath}")
else:
    arcpy.AddError(f"No development file found for the year {Year}")

#%% Mosaic all marsh files into one raster covering the entire study area
# Create output filename for the mosaicked marsh raster
mosaicked_marsh = os.path.join(output_data, f"marsh_mosaic_SLR_{slr_formatted}ft.tif")

# Mosaic all selected marsh files into one raster
arcpy.AddMessage(f"\n--- Mosaicking {len(selected_marsh_files)} marsh files ---")
arcpy.management.MosaicToNewRaster(
    input_rasters=selected_marsh_files,
    output_location=output_data,
    raster_dataset_name_with_extension=f"marsh_mosaic_SLR_{slr_formatted}ft.tif",
    pixel_type="8_BIT_UNSIGNED",  
    number_of_bands=1,
    mosaic_method="FIRST"  
)

arcpy.AddMessage(f"Mosaicked marsh file created: {mosaicked_marsh}")

#%% Create conflict zone using the mosaicked marsh and development file
# Use the development file (covers the entire study area)
dev_file = selected_dev_files[0]

# Create output filename for conflict zone
out_raster = os.path.join(output_data, f"con_zone_{Year}_SLR_{slr_formatted}ft.tif")

# Convert to absolute path
out_raster_absolute = os.path.abspath(out_raster)

# Load rasters and add them
marsh_raster = arcpy.Raster(mosaicked_marsh)
dev_raster = arcpy.Raster(dev_file)

# Add the rasters together
conflict_zone = marsh_raster + dev_raster

# Save the output
conflict_zone.save(out_raster_absolute)

arcpy.AddMessage(f"\n--- Conflict Zone Created ---")
arcpy.AddMessage(f"Output file: {out_raster_absolute}")
# Set the output parameter so it appears in the map
arcpy.SetParameterAsText(2, out_raster_absolute) 