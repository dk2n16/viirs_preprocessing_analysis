"""Main module to carry out analysis on rasters preprocessing in main.py"""
from pathlib import Path
from split_admin_units import SplitAdminUnits
from extract_rasters import ExtractFromRasters

def main(country):
    
    L1 = BASE_DIR.joinpath(f'shps/L1/{country}/{country}_adm1.shp')
    subnational = [x for x in BASE_DIR.joinpath(f'shps/L2_L3_L4/{country}').iterdir() if x.name.endswith('2.shp') if not x.name.endswith('1.shp')]
    sorted(subnational)
    L1_expl = L1.parent.joinpath('exploded')
    if not L1_expl.exists():
        L1_expl.mkdir(parents=True, exist_ok=True)
    SplitAdminUnits(L1, L1_expl, 1)
    for sub in subnational:
        level = sub.stem[-1]
        sub_expl = sub.parent.joinpath('exploded')
        level_folder = sub_expl.joinpath(f'{sub.stem}')
        if not level_folder.exists():
            level_folder.mkdir(parents=True, exist_ok=True)
        SplitAdminUnits(sub, level_folder, level)
        

def main_extract_subnational_rasters(country):
    YEARS = [x for x in BASE_DIR.joinpath(f'datain/{country}').iterdir()]
    L1 = BASE_DIR.joinpath(f'shps/L1/{country}/{country}_adm1.shp')
    L1_expl = L1.parent.joinpath('exploded')
    l1_list = [x for x in L1_expl.iterdir() if x.name.endswith('.shp')]

    L2 = BASE_DIR.joinpath(f'shps/L2_L3_L4/{country}/exploded/{country}_adm2')
    l2_list = [x for x in L2.iterdir() if x.name.endswith('.shp')]


    for year in YEARS:
            months = [x for x in year.iterdir() if not x.name == 'Annual_comp']
            for month in months:
                out_folder = month.joinpath('subnational')
                if not out_folder.exists():
                    out_folder.mkdir(parents=True, exist_ok=True)
                rad_raster = [x for x in month.iterdir() if x.name.endswith('masked_rad.tif')][0]
                for l1 in l1_list:
                    l1_out_folder = out_folder.joinpath('l1')
                    if not l1_out_folder.exists():
                        l1_out_folder.mkdir(parents=True, exist_ok=True)
                    name = l1_out_folder.joinpath(f'{country}_{l1.stem}_{month.name}_{year.name}.tif')
                    ExtractFromRasters(rad_raster, l1, name)

                for l2 in l2_list:
                    l2_out_folder = out_folder.joinpath('l2')
                    if not l2_out_folder.exists():
                        l2_out_folder.mkdir(parents=True, exist_ok=True)
                    name = l2_out_folder.joinpath(f'{country}_{l2.stem}_{month.name}_{year.name}.tif')
                    ExtractFromRasters(rad_raster, l2, name)
                





    #explode national shp and extract rasters

    #stack subnational raster (all jans; all febs etc) and find MIN, MAX, MEAN, MED, STD

    #make graphs

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    #countries = ['HTI', 'NAM', 'MOZ', 'GHA', 'NPL']
    countries = ['GHA', 'NPL']
    #countries = ['HTI']
    for country in countries:
        main(country)
        main_extract_subnational_rasters(country)