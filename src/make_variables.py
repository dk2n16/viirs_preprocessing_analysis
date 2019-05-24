"""Module to set up paths, variable and file names to pass to modules for VIIRS preprocessing and analysis"""
from pathlib import Path

class MakeVariables:
    """Class to set up variable and path names for analysis and preprocessing of VIIRS rasters
    
    Takes in:
        year --> Year to be analysed

        country --> ISO of country of interest

    Returns dictionary with the following set up:

        extent --> VIIRS tile to which country corresponds

        [shps] --> National and subnational shapefiles

        Annual composite --> Ave annual radiance that is closest to year being analysed

        rade9h --> radiance input raster

        cvg --> coverage/observation raster

        csv --> Table for zonal statistics at different levels (one file corresponding for each above subnational shp).    
    """

    COUNTRIES = {'HTI': '75N180W', 'GHA': '75N060W', 'MOZ': '00N060W', 'NAM': '00N060W', 'NPL': '75N060E'} #dictionary to hold VIIRS tiles regions corresponding to countries

    def __init__(self, country, year):
        """
        country --> input country (iso)
        year -> year of interest (2012 - 2018)
        """
        self.country = country
        self.year = year
        try:
            self.extent = self.COUNTRIES[self.country]
        except KeyError as e:
            print('This country is not set up for this analysis')
            print(e)
        self.BASEDIR = Path(__file__).resolve().parent.parent
        self.variables_paths = {}
        self.variables_paths.setdefault('L0', self.get_l0_path())
        self.variables_paths.setdefault('L1', self.get_l1_path())
        self.variables_paths.setdefault('subnational', self.get_subnational_paths())
        self.variables_paths.setdefault('ann_composite', self.get_annual_composite_path())
        self.variables_paths.setdefault('raw_rad9_tiles', self.get_raw_radiance_tif())

    def get_l0_path(self):
        """Returns path to national level shapefile"""
        path = self.BASEDIR.joinpath(f'shps/L0/{self.country}/{self.country.lower()}_level0_2000_2020.shp')
        return path

    def get_l1_path(self):
        """Returns path to L1 shapefiles"""
        path = self.BASEDIR.joinpath(f'shps/L1/{self.country}/{self.country}_adm1.shp')
        return path

    def get_subnational_paths(self):
        """Returns paths to subnational shapefiles"""
        paths = [x for x in self.BASEDIR.joinpath(f'shps/L2_L3_L4/{self.country}').iterdir() if x.name.endswith('shp')]
        return paths

    def get_annual_composite_path(self):
        """Returns path to annual composite (=< 2015 is 2015 OR >= 2016 is 2016)"""
        if self.year <= 2015:
            path = self.BASEDIR.parent.parent.joinpath(f'download_viirs_iridis/download_viirs_iridis/datain/Annual_2015_2016/SVDNB_npp_20150101-20151231_{self.extent}_vcm-orm-ntl_v10_c201701311200.avg_rade9.tif')
        else:
            path = self.BASEDIR.parent.parent.joinpath(f'download_viirs_iridis/download_viirs_iridis/datain/Annual_2015_2016/SVDNB_npp_20160101-20161231_{self.extent}_vcm-orm-ntl_v10_c201807311200.avg_rade9.tif')
        return path

    def get_raw_radiance_tif(self):
        """Returns path to raw radiance tile"""
        path = self.BASEDIR.joinpath()

    
