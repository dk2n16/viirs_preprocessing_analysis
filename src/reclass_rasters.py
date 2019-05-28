"""Reclass rasters using mask (either cvg raster to make radiance rasters nodata below the cvg threshold 
OR make radiance pixels 0 where annual composite is 0"""
import numpy as np 
import rasterio

class ReclassRasters:
    """Reclass rasters based on raster, mask and threshold value"""

    def __init__(self, in_raster, mask_raster, out_raster, threshold_value, output_value, remove_negative_values=False):
        """
        in_raster --> raster to reclassify
        mask_raster --> raster to use as mask
        out_raster --> output
        threshold_value --> value in mask
        output_value --> value to make pixels that fall outside mask
        remove_negative_values --> if true, remove all negative pixels (except ND pixels)
        """
        self.in_raster = in_raster
        self.mask_raster = mask_raster
        self.out_raster = out_raster
        self.threshold_value = threshold_value
        self.output_value = output_value
        self.remove_negative_values = remove_negative_values
        self.reclassify_raster()

    def reclassify_raster(self):
        """Reclassifies input raster to output value in pixels that fall outside of mask"""
        profile = self.make_profile_from_template()
        with rasterio.open(self.in_raster) as src, rasterio.open(self.mask_raster) as msk, rasterio.open(self.out_raster, 'w', **profile) as dst:
            src_data = src.read()
            msk_data = msk.read()
            src_data[np.where(msk_data == self.threshold_value)] = self.output_value
            if self.remove_negative_values:
                src_data[(src_data < 0) & (src_data != -99999)] = msk_data[(src_data < 0) & (src_data != -99999)]
            dst.write(src_data)

    def make_profile_from_template(self):
        """Make profile from original raster (ND etc)"""        
        template = rasterio.open(self.in_raster)
        profile = template.profile
        profile.update(
            count=1,
            compress='lzw',
            predictor=2,
            bigtiff='yes',
            nodata=-99999
        )
        template.close()
        return profile