"""
Created on Fri Jul 19 11:59:35 2019

@author: Jhon Valderrama

This module is the base layer for orthomosaics postprocessing work flow,
it contains the basics functions to operate rasters and shapes files.
 """
import rasterio
import numpy as np
from rasterio.mask import mask
import geopandas as gpd
from fiona import errors
from rasterstats import zonal_stats
import os
import json

# ------------------------------------------------------


def mask_ortho(path, file, mask_path, en=0):
    """This function makes a clip from a raster and vector files path
    Args:
        Path(str): Directory path for raster file
        File(str): Raster file name
        Mask_path(str): File path for vector
        en(int): Parameter that enables the output of raster clipped object
    Returns:
        there are 3 types of outputs:
            if any error : [1]
            list: list with 1 element which contains a file_path for raster
             clipped
            list: list with 2 element which contains a file_path for raster
             clipped and raster object respectively
    """

    fp = path + "\\" + file
#     print(fp)
#     print(mask_path)
    out_tif = path + "\\" + "ERASE" + "\\" + file
    out_tif = out_tif.replace(".tif", "_mask.tif")

    try:
        with rasterio.open(fp) as d:
            masking = gpd.read_file(mask_path)
            out, t = mask(d, [json.loads(masking.to_json())[
                          'features'][0]['geometry']], crop=True)
            out_meta = d.meta.copy()
            out_meta.update({"driver": "GTiff",
                             "height": out.shape[1],
                             "width": out.shape[2],
                             "transform": t,
                             "crs": d.crs})
        dest = rasterio.open(out_tif, "w+", **out_meta)
        dest.write(out)
        if en == 1:
            return [out_tif, dest]
        else:
            dest.close()
            return [out_tif]
    except rasterio.errors.RasterioIOError:
        return [1]
    except errors.DriverError:
        return [1]
    except BaseException:
        return [sys.exc_info()[0]]
# ------------------------------------------------------


def Vis_cal(fp):
    """This function makes the calculations for 9 VIs.
    Args:
        fp(str): Raster file path for extracting the VIs
    Returns:
        there are 2 types of outputs:
            if file is not found :  ["Raster Error: {0}".format(err1)]
            dictionary: with 9 VIs files path
    """

    ndvi_path = fp.replace(".tif", "_NDVI.tif")
    ndre_path = fp.replace(".tif", "_NDRE.tif")
    gndvi_path = fp.replace(".tif", "_GNDVI.tif")
    bndvi_path = fp.replace(".tif", "_BNDVI.tif")
    ervi_path = fp.replace(".tif", "_ERVI.tif")
    egvi_path = fp.replace(".tif", "_EGVI.tif")
    ebvi_path = fp.replace(".tif", "_EBVI.tif")
    grvi_path = fp.replace(".tif", "_GRVI.tif")
    gbvi_path = fp.replace(".tif", "_GBVI.tif")
    out_path = {
        "NDVI": ndvi_path,
        "NDRE": ndre_path,
        "GNDVI": gndvi_path,
        "BNDVI": bndvi_path,
        "ERVI": ervi_path,
        "EGVI": egvi_path,
        "EBVI": ebvi_path,
        "GRVI": grvi_path,
        "GBVI": gbvi_path}
    try:
        with rasterio.open(fp) as raster:
            out_meta = raster.meta.copy()
            out_meta.update({"driver": "GTiff", "height": raster.height,
                             "width": raster.width, "count": 1,
                             "transform": raster.transform, "crs": raster.crs,
                             "dtype": "float32"})
            blue = raster.read(1).astype(np.float32)
            green = raster.read(2).astype(np.float32)
            red = raster.read(3).astype(np.float32)
            rededge = raster.read(4).astype(np.float32)
            nir = raster.read(5).astype(np.float32)
        with rasterio.open(ndvi_path, "w+", **out_meta) as out:
            ndvi = np.where(
                (nir + red) == 0.,
                0,
                (nir - red) / (nir + red)
            )
            out.write(ndvi, 1)
            del ndvi
        with rasterio.open(ndre_path, "w+", **out_meta) as out:
            ndre = np.where(
                (nir + rededge) == 0.,
                0,
                (nir - rededge) / (nir + rededge)
            )
            out.write(ndre, 1)
            del ndre
        with rasterio.open(gndvi_path, "w+", **out_meta) as out:
            gndvi = np.where(
                (nir + green) == 0.,
                0,
                (nir - green) / (nir + green)
            )
            out.write(gndvi, 1)
            del gndvi
        with rasterio.open(bndvi_path, "w+", **out_meta) as out:
            bndvi = np.where(
                (nir + blue) == 0.,
                0,
                (nir - blue) / (nir + blue)
            )
            out.write(bndvi, 1)
            del bndvi
        with rasterio.open(ervi_path, "w+", **out_meta) as out:
            ervi = np.where(
                (rededge + red) == 0.,
                0,
                (rededge - red) / (rededge + red)
            )
            out.write(ervi, 1)
            del ervi
        with rasterio.open(egvi_path, "w+", **out_meta) as out:
            egvi = np.where(
                (rededge + green) == 0.,
                0,
                (rededge - green) / (rededge + green)
            )
            out.write(egvi, 1)
            del egvi
        with rasterio.open(ebvi_path, "w+", **out_meta) as out:
            ebvi = np.where(
                (rededge + blue) == 0.,
                0,
                (rededge - blue) / (rededge + blue)
            )
            out.write(ebvi, 1)
            del ebvi
        with rasterio.open(grvi_path, "w+", **out_meta) as out:
            grvi = np.where(
                (green + red) == 0.,
                0,
                (green - red) / (green + red)
            )
            out.write(grvi, 1)
            del grvi
        with rasterio.open(gbvi_path, "w+", **out_meta) as out:
            gbvi = np.where(
                (green + blue) == 0.,
                0,
                (green - blue) / (green + blue)
            )
            out.write(gbvi, 1)
            del gbvi
        # Clear memory
        del blue
        del green
        del red
        del rededge
        del nir
    except rasterio.errors.RasterioIOError as err1:
        return ["Raster Error: {0}".format(err1)]
    return out_path
# ------------------------------------------------------


def vegetation_extraction(fp, en=0):
    """This function makes the extraction of vegetation for an orthomosaic
       using the work of Yuan Wang et al. (2012)
    Args:
        fp(str): Raster file path for extracting the vegetation
        en(int): Parameter that enables the output of raster proccesed object
    Returns:
        there are 3 types of outputs:
            if file is not found : [1]
            list: list with 1 element which contains a file_path for
             raster proccesed
            list: list with 2 element which contains a file_path for
             raster proccesed and raster object respectively
    """
    out = fp.replace(".tif", "_extrac_veg.tif")
    try:
        with rasterio.open(fp) as raster:
            out_meta = raster.meta.copy()
            out_meta.update({"driver": "GTiff",
                             "height": raster.height,
                             "width": raster.width,
                             "count": raster.count,
                             "transform": raster.transform,
                             "crs": raster.crs,
                             "dtype": "float64"})
            r = raster.read().astype(np.float64)  # change to float32
                                                  # for less precision
            out_temp = np.where(  # Green minus red index
                r[1] - r[2] <= 20.,
                0,
                r
            )

        dest = rasterio.open(out, "w+", **out_meta)
        dest.write(out_temp)
        if en == 1:
            return [out, dest]
        else:
            dest.close()
            return [out]
        # return r
    except rasterio.errors.RasterioIOError:
        return [1]
# ------------------------------------------------------


def statistics_extraction(fp, shp):
    """This function return a list with a dictionary with statistics
    Args:
        fp(str): Raster file path for extracting the statistics
        shp(str): Shape file path for extracting the statistics
    Returns:
        there are 2 types of outputs:
            if file is not found error : [1]
            list: return a list with a dictionary with statistics
    """
    try:
        with rasterio.open(fp) as r:
            array = r.read(1)
            affine = r.transform
            data = gpd.read_file(shp)
        stat = zonal_stats(
            data,
            array,
            affine=affine,
            stats=[
                'min',
                'max',
                'mean',
                'median',
                'majority'])
        return stat  # return a list with a dictionary
    except rasterio.errors.RasterioIOError:
        return [1]
# ------------------------------------------------------
