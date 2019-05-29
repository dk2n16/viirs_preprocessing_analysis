"""
METHOD:
1. Extract radiance and coverage raster from global tiles for every country, for every month for every year
2. Make monthly radiance pixels NoData WHERE coverage raster pixels are 0
3. Make above output 0 WHERE annual composite is 0
****NOTE -- remaining NoData pixels are left as nodata
"""

from pathlib import Path
from make_variables import MakeVariables 
from extract_rasters import ExtractFromTiles
from reclass_rasters import ReclassRasters

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
        DATAIN_MONTH = BASEDIR.joinpath(f"{country}/{year}/{str(rad).split('/')[6]}")
        if not DATAIN_MONTH.exists():
            DATAIN_MONTH.mkdir(parents=True, exist_ok=True)
        name = f"{country}_{str(rad).split('/')[6]}_{year}_rad.tif"
        out_rad = DATAIN_MONTH.joinpath(name)
        ExtractFromTiles(rad, L0, out_rad)
        print(rad)
    for cvg in path_dict.variables_paths['raw_cvg_tiles']:
        DATAIN_MONTH = BASEDIR.joinpath(f"{country}/{year}/{str(cvg).split('/')[6]}")
        if not DATAIN_MONTH.exists():
            DATAIN_MONTH.mkdir(parents=True, exist_ok=True)
        name = f"{country}_{str(cvg).split('/')[6]}_{year}_cvg.tif"
        out_cvg = DATAIN_MONTH.joinpath(name)
        ExtractFromTiles(cvg, L0, out_cvg)

    months = [x for x in BASEDIR.joinpath(f'{country}/{year}').iterdir() if x.name != 'Annual_comp']
    for month in months:
        rad = [x for x in month.iterdir() if x.name.endswith('rad.tif')][0]
        cvg = [x for x in month.iterdir() if x.name.endswith('cvg.tif')][0]
        comp_raster = ann_out_raster
        #Make rad ND where cvg == 0
        rad_ND = month.joinpath(f'{country}_{month.name}_{year}_ND.tif')
        ReclassRasters(rad, cvg, rad_ND, 0, -99999)
        #Make rad_ND 0 where composite is 0
        rad_masked = month.joinpath(f'{country}_{month.name}_{year}_masked_rad.tif')
        ReclassRasters(rad_ND, comp_raster, rad_masked, 0, 0, remove_negative_values=True)



    

    


if __name__ == "__main__":
    #countries = ['HTI', 'NAM', 'MOZ', 'GHA', 'NPL']
    countries = ['NAM', 'MOZ', 'GHA', 'NPL']
    #years = [2012, 2013, 2014, 2015, 2016, 2017, 2018]
    years = [2012, 2013, 2014]
    #years = [2012]
    for country in countries:
        for year in years:
            main(country, year)

