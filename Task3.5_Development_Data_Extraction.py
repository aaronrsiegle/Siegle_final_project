# Name: Task3.5_Development_Data_Extraction
# Date: 12/8/2025
# Description: This script takes the subset of the ICLUS data (clipped to the study area - output of Task 3) and extracts the relevant land use classes for this analysis

#%% Import system modules 
import arcpy
import geopandas as gpd 
import pandas as pd 
import os
import glob

#%% Set workspace 
arcpy.env.workspace = "..\\Scratch"

# Define folders
raw_data = "..\\Data\\Processed\\Development"
output_data = "..\\Data\\Processed\\Development_Classes"

#%% Load in all the processed tif files and extract relevant land use values
# Define range 
ICLUS_years = range(2030, 2101, 10)
# Create dictionary 
ICLUS_data = {}

for year in ICLUS_years: 
    in_raster = os.path.join(raw_data, f"dev_{year}_NAD83_clipped.tif")
    out_raster = os.path.join(output_data, f"ICLUS_{year}_processed.tif")
    # Using the try-except formatting to build error trapping into the workflow
    try:
        print(f"\nProcessing year {year}...")
        # Extract relevant land use classes 
        dev_areas = arcpy.sa.Con(in_raster, in_raster, "", 
                                   "VALUE = 11 OR VALUE = 12 OR VALUE = 13 OR VALUE = 14")
        # Save the result
        dev_areas.save(out_raster)
        # Store in dictionary
        ICLUS_data[year] = out_raster
    except Exception as e:
        print(f"  ERROR processing {year}: {str(e)}")

# Summary message 
print(f"\n--- Processing Complete ---")
print(f"Successfully processed {len(ICLUS_data)} files")
print(f"Output files saved to: {output_data}")

#%%  
