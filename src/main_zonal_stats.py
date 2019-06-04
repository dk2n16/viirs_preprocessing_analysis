"""Main module to run zonal stats on all subnational units over all months over the years and per month"""
from pathlib import Path
from viirs_zonal_stats import IntraYearZonalStats
import pandas as pd

def main(BASEDIR, country, level, outfolder):
    zon = IntraYearZonalStats(BASEDIR, country, level, outfolder.joinpath(f'{country}_{level}_zonal_stats.csv'))
    
    

if __name__ == "__main__":
    BASEDIR = Path(__file__).resolve().parent.parent
    #countries = ['HTI', 'NAM', 'NPL', 'MOZ', 'GHA']
    countries = ['HTI']
    levels = ['l1', 'l2']
    #levels = ['l1']
    for country in countries:
        outfolder = BASEDIR.joinpath(f'dataout/{country}/zonal_stats/multiyear')
        if not outfolder.exists():
            outfolder.mkdir(parents=True, exist_ok=True)
        for level in levels:
            main(BASEDIR, country, level, outfolder)
            print(f'{country} {level} done')
