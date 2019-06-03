"""Class to make temporal boxplots of admin units"""
from pathlib import Path
import numpy as np
import pandas as pd
import rasterio
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt 
from sklearn.preprocessing import scale

BASEDIR = Path(__file__).resolve().parent.parent

class MakeBoxPlots:
    def __init__(self, country, unit, out_image, level, log=False, keep_zeros=False):
        """
        country: ISO
        unit: subnational unit name
        out_image: path to boxplot png
        level: admin unit leve
        log: Plot y-axis on logarithmic scale
        keep_zeros: (Boolean) consider 0 values in analysis

        """
        self.country = country
        self.unit = unit
        self.out_image = out_image
        self.level = level
        self.log = log #False as default
        self.keep_zeros = keep_zeros
        self.make_boxplots()

    def make_boxplots(self):
        years = range(2012, 2019)
        months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        temporal_units = []
        monthly_units = []
        for month in months:
            for year in years:
                raster = BASEDIR.joinpath(f'datain/{self.country}/{year}/{month}/subnational/{self.level}/{self.unit}_{month}_{year}.tif')
                if raster.exists():
                    with rasterio.open(raster) as src:
                        data = src.read(1)
                        if self.keep_zeros:
                            data = data[np.where((data!= -99999))]
                        else:
                            data = data[np.where((data!= -99999) &(data != 0))]
                        monthly_units.append(data)
            stack_month = np.concatenate(tuple(monthly_units), axis=0)
            temporal_units.append(stack_month)
        fig = plt.figure(figsize=(9,6))
        ax = fig.add_subplot(111)
        if self.log:
            plt.yscale('log')
        bp = ax.boxplot(temporal_units)
        fig.savefig(self.out_image, bbox_inches='tight')

                
