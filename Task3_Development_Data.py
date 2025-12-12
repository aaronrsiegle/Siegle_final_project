# Name: Task3_Development_Data_Prep
# Date: 12/4/2025
# Description: This script takes the outputs of the ICLUS model, reprojects them and subsets them to the study area

#%% Import system modules 
import arcpy
import geopandas as gpd 
import pandas as pd 
import os
import glob

#%% Set workspace 
arcpy.env.workspace = "..\\Scratch"

# Define folders
raw_data = "..\\Data\\Raw\\Development"
output_data = "..\\Data\\Processed\\Development"

#%% Define base directory
base_dir = '..\\Data\\Raw\\Development'  

#%% Load in all the tif files 
# Define range
years = range(2030, 2101, 10)
# Define target projection (NAD83)
target_sr = arcpy.SpatialReference(26918) # NAD 1983 UTM Zone 18N
print(f"\nTarget projection: {target_sr.name}")

#%% Creating input variables needed for the analysis step 
study_area = "..\\Data\\Processed\\Study_Area\\Study_Area_Counties.shp"

# Create dictionary 
processed_dict = {}

#%% Reprojecting the ICLUS rasters and clipping them to the study area 
# Warning: This code chunk runs for extended periods of time
for year in years:
    # Input raster
    in_raster = os.path.join(raw_data, f"ICLUS_v2_1_1_land_use_conus_{year}_ssp2_rcp45_hadgem2_es.tif") 
    # Output raster (reprojected and clipped)
    out_raster = os.path.join(output_data, f"dev_{year}_NAD83_clipped.tif")
    # Temporary reprojected raster
    temp_reproject = os.path.join(arcpy.env.workspace, f"temp_reproj_{year}.tif")
    # Using the try-except formatting to build error trapping into the workflow
    try:
        print(f"\nProcessing year {year}...")
        
        # Reproject to NAD 1983 UTM Zone 18N
        print(f"  Reprojecting to NAD 1983 UTM Zone 18N...")
        arcpy.management.ProjectRaster(
            in_raster=in_raster,
            out_raster=temp_reproject,
            out_coor_system =target_sr,
            resampling_type="NEAREST"  
        )
        
        # Clip to study area
        print(f"  Clipping to study area...")
        arcpy.management.Clip(
            in_raster=temp_reproject,
            rectangle="",  # Leave empty to use clip feature
            out_raster=out_raster,
            in_template_dataset=study_area,
            nodata_value="",
            clipping_geometry="ClippingGeometry",  # Clip to exact polygon shape
            maintain_clipping_extent="NO_MAINTAIN_EXTENT"
        )
        
        # Store in dictionary
        processed_dict[year] = out_raster
        
        # Clean up temporary files from memory
        arcpy.Delete_management("in_memory")
        
        print(f"  Successfully processed {year}")
        
    except Exception as e:
        print(f"  ERROR processing {year}: {str(e)}")
        # Clean up temporary files if error occurs
        arcpy.Delete_management("in_memory")

# Summary
print(f"\n--- Processing Complete ---")
print(f"Successfully processed {len(processed_dict)} files")
print(f"Output files saved to: {output_data}")

# Display processed years
if processed_dict:
    print(f"\nProcessed years: {list(processed_dict.keys())}")
    
    # Check one output
    if 2030 in processed_dict:
        out_desc = arcpy.Describe(processed_dict[2030])
        print(f"\n2030 output projection: {out_desc.spatialReference.name}")
        print(f"2030 extent: {out_desc.extent}")
else:
    print("\nNo files were successfully processed. Check error messages above.")
# %%
