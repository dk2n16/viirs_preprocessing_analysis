from pathlib import Path
from make_variables import MakeVariables 
from extract_rasters import ExtractFromTiles

BASEDIR = Path(__file__).resolve().parent.parent.joinpath('datain')

def main(country, year):
    path_dict = MakeVariables(country, year)
    L0 = path_dict.variables_paths['L0']
    ann_comp = path_dict.variables_paths['ann_composite']
    DATAIN_ANN = BASEDIR.joinpath(f'{country}/{year}/Annual_comp')
    if not DATAIN_ANN.exists():
        DATAIN_ANN.mkdir(parents=True, exist_ok=True)
    ann_out_raster = DATAIN_ANN.joinpath(f'{country}_Annual_comp_{year}.tif')
    ExtractFromTiles(ann_comp, L0, ann_out_raster)
    for rad in path_dict.variables_paths['raw_rad9_tiles']:
        DATAIN_MONTH = BASEDIR.joinpath(f'{country}/{year}/{str(rad).split('/')[6]}')
        if not DATAIN_MONTH.exists():
            DATAIN_MONTH.mkdir(parents=True, exists_ok=True)
        name = f"{country}_{str(rad).split('/')[6]}_{year}_rad.tif"
        out_rad = DATAIN_MONTH.joinpath(name)
        ExtractFromTiles(rad, L0, out_rad)
        print(rad)
    for cvg in path_dict.variables_paths['raw_cvg_tiles']:
        DATAIN_MONTH = BASEDIR.joinpath(f'{country}/{year}/{str(cvg).split('/')[6]}')
        if not DATAIN_MONTH.exists():
            DATAIN_MONTH.mkdir(parents=True, exists_ok=True)
        name = f"{country}_{str(cvg).split('/')[6]}_{year}_cvg.tif"
        out_cvg = DATAIN_MONTH.joinpath(name)
        ExtractFromTiles(cvg, shp, out_cvg)
    


if __name__ == "__main__":
    countries = ['HTI']
    #years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    years = [2012]
    for country in countries:
        for year in years:
            main(country, year)

