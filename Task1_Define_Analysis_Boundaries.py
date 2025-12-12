# Name: Task1_Define_Analysis_Boundaries
# Date: 12/1/2025 
# Description: This script takes all the counties in the United States from the USA Counties shapefile and subsets them based on a reference csv to create the study area boundaries

#%% Import system modules 
import arcpy
import geopandas as gpd
import pandas as pd

#%% Set workspace 
arcpy.env.workspace = "..\\Siegle_final_project"

# Define folders
raw_data = "..\\Data\\Raw\\Counties"
output_data = "..\\Data\\Processed\\Study_Area"

#%% Import county data 
USAcounties_file_path = "..\\Data\\Raw\\Counties\\USA_Counties_2615615788148899056\\USA_Counties.shp"
USACounties = gpd.read_file(USAcounties_file_path)

# View county data 
print(USACounties.head())
print(f"\nCRS: {USACounties.crs}")
print(f"Geometry type: {USACounties.geometry.type.unique()}")

#%% Import study area boundaries 
SAcounties = pd.read_excel("..\\Data\\Raw\\Counties\\County_Typologies_GIS_V2.xlsx", sheet_name= "Data")
print(SAcounties)

#%% Subsetting USA Counties with study area 
SACounties_Joined = USACounties.merge(SAcounties, 
                                      left_on= ['NAME', 'STATE_NAME'],  
                                      right_on= ['CO_Name', 'State'], 
                                      how='inner')  
print(SACounties_Joined)

# Saving the result as a shapefile
output_path = f"{output_data}\\Study_Area_Counties.shp"
SACounties_Joined.to_file(output_path)
print(f"\nSaved to: {output_path}")

# %%
