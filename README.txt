Marsh Migration Simulation Tool 
Date: 12/9/2025
Author: Aaron Siegle 
Contact info: aaron.siegle@duke.edu 
For the completion of the final project for ENV859 - Geospatial Data Analytics 
Institution: Duke University, Nicholas School of the Environment 

Project Title: Mapping marsh migration across 6 mid-Atlantic states based on multiple development and sea level rise scenarios 

Summary: The tool takes input raster dataset from the US EPA’s Integrated Climate and Land Use Scenarios (ICLUS) model and NOAA’s Coastal Change Analysis Program (CCAP) to build a raster dataset of the marsh migration corridor areas that are likely to be developed.  

User defined inputs:  

- Year of projection (between 2030 and 2100, in 10-year increments)  
- Sea Level Rise Value (In Feet) From 0.5 ft to 10.0 ft, in half-foot increments (e.g., 0.5, 1.0, 1.5, etc.). 

Model outputs:  

The model will create a dataset of 90x90 meter raster cells across the six-state region that represent the marsh-migration corridor areas that are most likely to be developed given the user-defined parameters  

Data:  

ICLUS model: raster dataset of projected land use across the continental United States

90x90m cells  

Link: https://www.epa.gov/gcx/iclus-downloads 

CCAP data: shows how coastline/marsh dynamics will change based on certain SLR scenarios  

Datasets are segmented out by state and projected SLR (by 0.5 ft increments)  

10x10m cells  

Link: https://coastalimagery.blob.core.windows.net/ccap-landcover/CCAP_bulk_download/Sea_Level_Rise_Wetland_Impacts/index.html

Feature class of USA counties from the ESRI data repository 

For complete pseudocode/workflow, see Pseudocode-Workflow file in the docs folder 

5 python scripts were created to conduct the necessary data cleaning and analysis for this project. Note that the Task 2 and Task 3 scripts take roughly 60-90 minutes to run. However, these scripts only needed to be run once to create the files that serve as inputs for Task 4, which is the script behind the Marsh Migration Simulation Geoprocessing Tool in ArcGIS Pro. This tool takes roughly 2 minutes to run. 

The final output of this tool is the Marsh Migration Simulation Geoprocessing Tool. This tool can be found in the toolbox of the V:\Siegle_final_project\Siegle_Final_Project.aprx ArcGIS Pro Project


