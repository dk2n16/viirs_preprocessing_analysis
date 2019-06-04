"""Main module to run zonal stats on all subnational units over all months over the years and per month"""
from pathlib import Path
from viirs_zonal_stats import IntraYearZonalStats, MonthlyZonalStats
import pandas as pd

def main(BASEDIR, country, level, outfolder):
    zon = IntraYearZonalStats(BASEDIR, country, level, outfolder.joinpath(f'{country}_{level}_zonal_stats.csv'))

def main_zonal_monthly(BASEDIR, country, outfolder_monthly):
    #years = range(2012, 2019)
    years = [2012]
    shp1 = BASEDIR.joinpath(f'shps/L1/{country}/{country}_adm1.shp')
    shps = [x for x in BASEDIR.joinpath(f'shps/L2_L3_L4/{country}').iterdir() if x.name.endswith('shp') if not x.name.endswith('1.shp')]
    shps.append(shp1)
    for year in years:
        outfolder_year = outfolder_monthly.joinpath(f'{year}')
        if not outfolder_year.exists():
            outfolder_year.mkdir(parents=True, exist_ok=True)
        for shp in shps:
            out_table = outfolder_monthly.joinpath(f'{shp.stem}_{year}.csv')
            zon = MonthlyZonalStats(BASEDIR, country, year, shp, out_table)
    
    

if __name__ == "__main__":
    BASEDIR = Path(__file__).resolve().parent.parent
    #countries = ['HTI', 'NAM', 'NPL', 'MOZ', 'GHA']
    countries = ['HTI']
    levels = ['l1', 'l2']
    #levels = ['l1']
    for country in countries:
        outfolder = BASEDIR.joinpath(f'dataout/{country}/zonal_stats/multiyear')
        outfolder_monthly = outfolder.parent.joinpath('monthly')
        if not outfolder.exists():
            outfolder.mkdir(parents=True, exist_ok=True)
        if not outfolder_monthly.exists():
            outfolder_monthly.mkdir(parents=True, exist_ok=True)
        for level in levels:
            #main(BASEDIR, country, level, outfolder) ########NEEDS TO BE REMOVED
            pass

        main_zonal_monthly(BASEDIR, country, outfolder_monthly)
        print(f'{country} {level} done')
