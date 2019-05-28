"""Module to extract rasters from global datasets using shapefiles"""
from pathlib import Path
import fiona
import rasterio
import rasterio.mask

class ExtractFromTiles:
    """Initialisation function

    in_raster --> Input VIIRS in_raster
    shp --> Shapefile from which to extract raster
    out_raster --Output file name

    returns None
    """
    def __init__(self, in_raster, shp, out_raster):
        self.in_raster = in_raster
        self.shp = shp
        self.out_raster = out_raster
        if 'rade9' in self.in_raster.name:
            self.nodata = -99999
        else:
            self.nodata = 255
        self.clip_raster()

    def clip_raster(self):
        with fiona.open(str(self.shp), 'r') as shapefile:
            features = [feature["geometry"] for feature in shapefile]

        with rasterio.open(str(self.in_raster)) as src:
            out_image, out_transform = rasterio.mask.mask(src, features, nodata=-99999, crop=True)
            out_meta = src.meta.copy()
        
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "count": 1,
            "compress": 'lzw',
            "predictor": 2,
            "bigtiff": "yes",
            'nodata': self.nodata
        })
        with rasterio.open(str(self.out_raster), 'w', **out_meta) as dst:
            dst.write(out_image)    


