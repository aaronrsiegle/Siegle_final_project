# Name: Task2_Marsh_Migration_Data_Prep
# Date: 12/2/2025 
# Description: This script takes the raw marsh migration data, subsets it, cleans it and extracts the relevant salt marsh classes for this analysis 

#%% Import system modules 
import arcpy
import RasterConversion
import geopandas as gpd
import pandas as pd
import os
import glob
from pathlib import Path

#%% Set workspace 
arcpy.env.workspace = "..\\Scratch"

# Define folders
raw_data = "..\\Data\\Raw\\Marsh_Migration"
output_data = "..\\Data\\Processed\\Marsh_Migration"

#%% Define base directory
base_dir = '..\\Data\\Raw\\Marsh_Migration'  

#%% Loading in all the tif files 
print("\n\nNested dictionary by state and SLR")
print("-" * 60)

states = ['MD', 'VA', 'NC', 'DE', 'NJ', 'NY']  
tif_data = {}

for state in states:
    state_folder = os.path.join(base_dir, state)
    if not os.path.exists(state_folder):
        continue
    
    tif_data[state] = {}
    
    # Get all tif files in state folder
    tif_files = glob.glob(os.path.join(state_folder, '*.tif'))
    
    for tif_path in tif_files:
        filename = os.path.basename(tif_path)
        if '_marshmigration_' in filename:
            # Split and get the last part before .tif
            slr_str = filename.split('_marshmigration_')[-1].replace('.tif', '')
            
            try:
                # Convert to float and divide by 10 to get feet 
                slr_value = float(slr_str) / 10.0
                tif_data[state][slr_value] = tif_path
            except ValueError:
                print(f"  Warning: Could not parse SLR from {filename}")
        else:
            print(f"  Warning: Unexpected filename format: {filename}")

#%% Structure of all the files 
for state in tif_data:
    print(f"\n{state}:")
    for slr in sorted(tif_data[state].keys()):
        print(f"  {slr} ft: {os.path.basename(tif_data[state][slr])}")

#%% Access a specific file 
print("\n\nExample Access:")
print("-" * 60)
print("To get Maryland 3.5 ft SLR file:")
if 'MD' in tif_data and 3.5 in tif_data['MD']:
    print(f"  Path: {tif_data['MD'][3.5]}")
#%% Creating input variables needed for the analysis step 
SA_Counties = "..\\Data\\Processed\\Study_Area\\Study_Area_Counties.shp"


#%% Apply geoprocessing tools to all the files 
# Warning: This code chunk takes roughly 60 minutes to process all the files 
print("\n\nExample Iteration:")
print("-" * 60)
print("Processing all files:")
for state, slr_dict in tif_data.items():
    for slr_value, filepath in slr_dict.items():
        print(f"  Processing {state} at {slr_value} ft SLR") 
        # Using the try-except formatting to build error trapping into the workflow 
        try:
            # Subsetting marsh migration data to the study area boundaries  
            SLR_subset = arcpy.sa.ExtractByMask(in_raster=filepath, 
                                                in_mask_data=SA_Counties)
            # Extracting the relevant marsh classes from all land cover types
            MM_areas = arcpy.sa.Con(SLR_subset, SLR_subset, "", 
                                   "VALUE = 13 OR VALUE = 14 OR VALUE = 17 OR VALUE = 18 OR VALUE = 19")
            
            # Systematically naming and exporting features
            output_filename = f"{state}_SLR_{str(slr_value).replace('.', '_')}ft_processed.tif"
            output_path = os.path.join(output_data, output_filename)
            
            # Save the raster
            MM_areas.save(output_path)
            
            print(f"    Saved to: {output_path}")
            
        except Exception as e:
            print(f"    Error processing {state} {slr_value} ft: {str(e)}")
            continue

# %%
