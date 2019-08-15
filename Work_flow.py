"""This module is a work flow for orthomosaics posproccesing, it contains the models for extract the statistics """
import rasterio
import numpy as np
from rasterio.mask import mask
import geopandas as gpd
from fiona import errors
import json
import os
from rasterstats import zonal_stats
# ------------------------------------------------------
def mask_ortho(path,file,mask_path,en=None):
    """This function makes a clip from a raster and vector files path
    
    Args:
        Path(str): Directory path for raster file
        File: Raster file name
        Mask_path: File path for vector
        en: Parameter that enables the output of raster clipped object
    Returns: 
        there are 3 kind of output:
            if any error : [1]
            list: list with 1 element which contains a file_path for raster clipped
            list: list with 2 element which contains a file_path for raster clipped and raster object respectively
    """

    fp=path + "\\" + file 
#     print(fp)
#     print(mask_path)
    out_tif = path + "\\" + "ERASE" + "\\" + file
    out_tif=out_tif.replace(".tif","_mask.tif")
    
    try:
        with rasterio.open(fp) as d:
            masking= gpd.read_file(mask_path)
            out, t = mask(d, [json.loads(masking.to_json())['features'][0]['geometry']], crop=True)
            out_meta=d.meta.copy()
            out_meta.update({"driver": "GTiff", "height": out.shape[1], "width": out.shape[2],
                             "transform": t,"crs": d.crs})
        dest=rasterio.open(out_tif, "w+", **out_meta)
        dest.write(out)
        if en==1:
            return [out_tif,dest]
        else:
            dest.close()
            return [out_tif]
    except rasterio.errors.RasterioIOError:
        return [1]  
    except errors.DriverError:
        return [1]
    except:
        return [sys.exc_info()[0]]
# ------------------------------------------------------
def Vis_cal(fp):
    ndvi_path=fp.replace(".tif","_NDVI.tif")
    ndre_path=fp.replace(".tif","_NDRE.tif")
    gndvi_path=fp.replace(".tif","_GNDVI.tif")
    bndvi_path=fp.replace(".tif","_BNDVI.tif")
    ervi_path=fp.replace(".tif","_ERVI.tif")
    egvi_path=fp.replace(".tif","_EGVI.tif")
    ebvi_path=fp.replace(".tif","_EBVI.tif")
    grvi_path=fp.replace(".tif","_GRVI.tif")
    gbvi_path=fp.replace(".tif","_GBVI.tif")
    out_path={"NDVI":ndvi_path, "NDRE":ndre_path,"GNDVI":gndvi_path,"BNDVI":bndvi_path,
              "ERVI":ervi_path,"EGVI":egvi_path,"EBVI":ebvi_path,"GRVI":grvi_path,"GBVI":gbvi_path}
    try:
        with rasterio.open(fp) as raster:
            out_meta=raster.meta.copy()
            out_meta.update({"driver": "GTiff", "height": raster.height, "width": raster.width,"count" : 1,
                             "transform": raster.transform,"crs": raster.crs,"dtype":"float32"})
            blue=raster.read(1).astype(np.float32)
            green=raster.read(2).astype(np.float32)
            red = raster.read(3).astype(np.float32)
            rededge=raster.read(4).astype(np.float32)
            nir = raster.read(5).astype(np.float32)
        with rasterio.open(ndvi_path, "w+", **out_meta) as out:
            ndvi=np.where(
                (nir+red)==0.,
                0,
                (nir-red)/(nir+red)
            )
            out.write(ndvi,1)
            del ndvi
        with rasterio.open(ndre_path, "w+", **out_meta) as out:
            ndre=np.where(
                (nir+rededge)==0.,
                0,
                (nir-rededge)/(nir+rededge)
            )
            out.write(ndre,1)
            del ndre
        with rasterio.open(gndvi_path, "w+", **out_meta) as out:
            gndvi=np.where(
                (nir+green)==0.,
                0,
                (nir-green)/(nir+green)
            )
            out.write(gndvi,1)
            del gndvi
        with rasterio.open(bndvi_path, "w+", **out_meta) as out:
            bndvi=np.where(
                (nir+blue)==0.,
                0,
                (nir-blue)/(nir+blue)
            )
            out.write(bndvi,1)
            del bndvi
        with rasterio.open(ervi_path, "w+", **out_meta) as out:
            ervi=np.where(
                (rededge+red)==0.,
                0,
                (rededge-red)/(rededge+red)
            )
            out.write(ervi,1)
            del ervi
        with rasterio.open(egvi_path, "w+", **out_meta) as out:
            egvi=np.where(
                (rededge+green)==0.,
                0,
                (rededge-green)/(rededge+green)
            )
            out.write(egvi,1)
            del egvi
        with rasterio.open(ebvi_path, "w+", **out_meta) as out:
            ebvi=np.where(
                (rededge+blue)==0.,
                0,
                (rededge-blue)/(rededge+blue)
            )
            out.write(ebvi,1)
            del ebvi
        with rasterio.open(grvi_path, "w+", **out_meta) as out:
            grvi=np.where(
                (green+red)==0.,
                0,
                (green-red)/(green+red)
            )
            out.write(grvi,1)
            del grvi
        with rasterio.open(gbvi_path, "w+", **out_meta) as out:
            gbvi=np.where(
                (green+blue)==0.,
                0,
                (green-blue)/(green+blue)
            )
            out.write(gbvi,1)  
            del gbvi
        del blue
        del green
        del red
        del rededge
        del nir
    except rasterio.errors.RasterioIOError as err1:
        return ["Raster Error: {0}".format(err1)]  
    return out_path
# ------------------------------------------------------
def extract_veg(fp,en):
    out = fp.replace(".tif","_extrac_veg.tif")
    try:
        with rasterio.open(fp) as raster:
            out_meta=raster.meta.copy()
            out_meta.update({"driver": "GTiff", "height": raster.height, "width": raster.width,"count" : raster.count,
                             "transform": raster.transform,"crs": raster.crs,"dtype":"float32"})
            r=raster.read().astype(np.float32)
            out_temp=np.where(
                r[1]-r[2]<=20.,
                0,
                r
            )
            
        dest=rasterio.open(out, "w+", **out_meta)
        dest.write(out_temp)
        if en==1:
            return [out, dest]
        else:
            dest.close()
            return [out]
        return r
    except rasterio.errors.RasterioIOError:
        return [1] 
# ------------------------------------------------------
def stat(fp,shp):
    try:
        with rasterio.open(fp) as r:
            array = r.read(1)
            affine = r.transform
            data=gpd.read_file(shp)
        stat = zonal_stats(data, array, affine=affine, stats=['min', 'max', 'mean', 'median', 'majority'])
        return stat # return a list with dictionaries 
    except rasterio.errors.RasterioIOError:
        return [1]
# ------------------------------------------------------
def ini(DIR,stage_feat=None):
    if stage_feat== None:
        a = os.walk(DIR)
        data=next(a)
        stages=data[1]
        stages.remove("SHAPES")
        stage_numbers=len(stages)
        variable= stages
        
    else:
        variable=[stage_feat]
        stage_numbers=1
    d={}
    for j in range(stage_numbers):    
        
        
        aux=os.walk(DIR + "\\" + variable[j] )
        temp=next(aux)
        
        
        file_names=temp[2]
        string=[]
        file_path2={}
        for i in range(len(file_names)):      
            string.append(file_names[i][0:file_names[i].find(".")].split("_"))
            if "RM" in string[i]:
                file_path2["RM"]=[temp[0], file_names[i],string[i][1:len(string[i])]]
            elif "THM" in string[i]:
                file_path2["THM"]=[temp[0],file_names[i],string[i][1:len(string[i])]]
            elif "DEM" in file_names[i]:
                file_path2["DEM"]=[temp[0],file_names[i],string[i][1:len(string[i])]]
        d[variable[j]]=file_path2
    return d
# ------------------------------------------------------
def to_mask(Dir,cycle,stage_feat=None):
    d=ini(Dir,stage_feat)
    mask=Dir + "\\" + "SHAPES" + "\\" + "ALL.shp"
    plots=Dir + "\\" + "SHAPES" + "\\" + "PLOTS.shp"
    out= r"C:\Users\Usuario\gis\CASANARE\DRONES\DATA\CIMARRON" +"\\" + cycle + "\\" + cycle + "_" + "STAT.json"
    dic={}
    ortho={}
    for i in d:
        ortho={}
        if "RM" in d[i]:
            ma=mask_ortho(d[i]["RM"][0],d[i]["RM"][1],mask,0)
#             print(ma)
#             print(d[i]["RM"][0])
#             print(d[i]["RM"][1])
#             print(mask)
            if  ma!= [1]:
                e=extract_veg(ma[0],0)
                # anexar error al archivo log
                if e!=1:
                    path=Vis_cal(e[0])
            del ma
            del e
#             print(path)
#             print(len(path))
#             print(plots)
            dic_RM={}
            for j in path:
                dic_RM[j]=stat(path[j],plots)
            ortho["RM"]=dic_RM #[stat(path[i],plots) for i in range(len(path))]
#             delete variable
            del dic_RM
            del path
        
#        if "THM" in d[i]:
#            ma=mask_ortho(d[i]["THM"][0],d[i]["THM"][1],mask,0)
            
#            ortho["THM"]=[stat(path[i],plots) for i in range(len(path))]
            
        if "DEM" in d[i]:
            ma=mask_ortho(d[i]["DEM"][0],d[i]["DEM"][1],mask,0)
            if  ma!= [1]:
                ortho["DEM"]=stat(ma[0],plots)
            del ma
        print(ortho)
        dic[i]=ortho
        
    json_file = json.dumps(dic)
    f = open(out,"w")
    f.write(json_file)
    f.close()
    return out
  
    