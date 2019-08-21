# Work Flow for Postprocessing Orthomosaics
The Objective of this project is to consolidate the VIs data, agronomic data
and greenhouse gases data.

## There are some requirements to run this algorithm:
### 1) Minimum machine requirements:
  - 16 Gb of ram
  - Core i5(8th gen)
### 2) Sowtfware requirements:
  - Anaconda:
    - rasterio
    - pandas
    - geopandas
    - rasterstats
    - fiona
    - numpy
  - git
  - github

### 3) To create a directory path as follows:
## For orthomosaics:
 "MAINFOLDER\LOCATION\DRONES\MAPS\CIMARRON\FIELD\ALL\CYCLE"

The orthomosaics must be organized in folders with their respective crop stage name. This names must begin with the order number the crop stages were sampled, ie, 0_MAXTILLERING, 1_BOOTING, etc. in this example if maxtillering stage is not sampled, the booting stage name will be 0_BOOTING.
### For consolidated dataframe of VIS and agronomic data and graphics:
    "MAINFOLDER\LOCATION\DRONES\DATA\CIMARRON\FIELD\ALL\CYCLE"
This path will be use to save the consolidate data and graphics



## There is 3 layers:
### 1) Base layer:
This layer contains the basics funtions to operate betwen rasters
   and shapes files.
### 2) Contoller layer:
This layer contains the functions to use the basics funtions to procces all the orthomosaic in the directory path.
### 3) visualization layer:
