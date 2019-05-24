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

    def get_l0_path(self):
        """Returns path to national level shapefile"""
        pass
