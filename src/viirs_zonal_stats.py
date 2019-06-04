"""Module with classes to calculate zonal statistics with all years stacked (IntraYearZonalStats) and individual years (MontlyZonalStats).

IntraYearZonalStats --> Class will read array of individual admin units for each month over all the years. All months will be stacked into individual 3D array per month (1 3D array for JAN, 1 3D array for FEB etc.) and calculate the summary statistics over the years per month (COUNT, SUM, MIN, MEAN, MAX, STD, MED, %LIT, %UNLIT). Will 1 output table for all years.

MonthlyZonalStats --> Class will calculate conventional zonal stats for the whole country delineated by admin unit levels for each month in each year (COUNT, SUM, MIN, MEAN, MAX, STD, MED, %LIT, %UNLIT, %NoData). Will output a table for each year. Should include the annual composite.
"""
from pathlib import Path
from rasterstats import zonal_stats
import rasterio
import pandas as pd
import numpy as np
import geopandas as gpd
from functools import reduce

class IntraYearZonalStats:
    """Class to extract each year's subnational rasters, stack months and do zonal stats for those months"""
    def __init__(self, BASEDIR, country, level, out_table):
        self.BASEDIR = BASEDIR
        self.country = country
        self.level = level
        self.out_table = out_table
        self.shp = self.get_shp()
        self.units = self.get_unit_names()
        self.df_to_concat = []
        #self.df = self.make_dataframe()
        self.loop_through_years()
        self.concat_dataframes()

        
    def get_shp(self):
        """Get relevant shapefile to carry out zonal stats"""
        if self.level == 'l1':
            shp = self.BASEDIR.joinpath(f'shps/L1/{self.country}/{self.country}_adm1.shp')
        else:
            shp = self.BASEDIR.joinpath(f'shps/L2_L3_L4/{self.country}/{self.country}_adm{self.level[-1]}.shp')
        return shp
    
    def get_unit_names(self):
        """Get subnational names"""
        units = ['_'.join(x.name.split('_')[0:-2]) for x in self.BASEDIR.joinpath(f'datain/{self.country}/2013/01/subnational/{self.level}').iterdir()]
        return units

    def make_dataframe(self):
        """Returns data frame of unit names/ids to which statistics can be appended"""
        adm_id = [x.split('_')[2] for x in self.units]
        adm_name = [x.split('_')[1] for x in self.units]
        df = pd.DataFrame({'adm_id': adm_id, 'adm_name': adm_name})
        return df
    
    def loop_through_years(self):
        """Get paths to all years' rasters for each month and pass datasets to calc_zonal_stats"""
        years = range(2012, 2019)
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        for unit in self.units:
            df_units = []
            for month in months:
                arrays_to_stack = []
                for year in years:
                    subnational_folder = self.BASEDIR.joinpath(f'datain/{self.country}/{year}/{month}/subnational/{self.level}')
                    if subnational_folder.exists():
                        raster = subnational_folder.joinpath(f'{unit}_{month}_{year}.tif')
                        data = self.read_raster(raster)
                        arrays_to_stack.append(data)
                stacked_arrays = np.stack(arrays_to_stack)
                df_month = self.calc_zonal_stats(stacked_arrays, unit, month)
                df_units.append(df_month)
            #df_all_months_for_unit = pd.concat(df_units, axis=1, on=)
            df_all_months_for_unit = reduce(lambda df1,df2: pd.merge(df1,df2,on=['adm_id', 'adm_name']), df_units)
            self.df_to_concat.append(df_all_months_for_unit)

    def read_raster(self, raster):
        """Returns numpy array of raster's pixel values"""
        with rasterio.open(raster) as src:
            data = src.read(1)
            return data          

    def calc_zonal_stats(self, stacked_arrays, unit, month):
        """Calculate summary statistics of stacked 3d array and append stats to dataframe corresponding to its admin unit (row) and month (col) in the i"""
        stacked_arrays[stacked_arrays < 0] = np.nan 
        minimum = np.nanmin(stacked_arrays)
        maximum = np.nanmax(stacked_arrays)
        mean = np.nanmean(stacked_arrays)
        median = np.nanmedian(stacked_arrays)
        std = np.nanstd(stacked_arrays)

        ################### Stats not considering unlit(0) pixels ############
        stacked_arrays[stacked_arrays == 0] = np.nan
        minimum_no_0 = np.nanmin(stacked_arrays)
        maximum_no_0 = np.nanmax(stacked_arrays)
        mean_no_0 = np.nanmean(stacked_arrays)
        median_no_0 = np.nanmedian(stacked_arrays)
        std_no_0 = np.nanstd(stacked_arrays)

        df_row = pd.DataFrame({'adm_id': [unit.split('_')[2]], 'adm_name': [unit.split('_')[1]], f'min_{month}': [minimum], f'max_{month}': [maximum], f'mean_{month}': [mean], f'median_{month}': [median], f'std_{month}': [std], f'min_no_0_{month}': [minimum_no_0], f'max_no_0_{month}': [maximum_no_0], f'mean_no_0_{month}': [mean_no_0], f'median_no_0_{month}': [median_no_0], f'std_no_0_{month}': [std_no_0]})
        df_row.set_index('adm_id')
        #self.df = pd.concat([self.df, df_row], axis=1)
        return df_row

    def concat_dataframes(self):
        """Saves all summary statistics for all units to dataframe/csv"""
        df = pd.concat(self.df_to_concat)
        df.to_csv(self.out_table, index=False)

        
        
