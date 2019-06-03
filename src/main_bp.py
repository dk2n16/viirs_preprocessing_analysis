from pathlib import Path
from make_boxplots import MakeBoxPlots

def main(country, adm_units, level):
    for unit in adm_units:
        out_image = BASEDIR.joinpath(f'dataout/{country}/boxplots/{level}/{unit}_12-18_no_zeros.png')
        out_image_zeros = BASEDIR.joinpath(f'dataout/{country}/boxplots/{level}/{unit}_12-18_zeros.png')
        out_image_log = out_image.parent.joinpath(f'{unit}_12-18_log_no_zeros.png')
        out_image_log_zeros = out_image.parent.joinpath(f'{unit}_12-18_log_zeros.png')
        if not out_image.parent.exists():
            out_image.parent.mkdir(parents=True, exist_ok=True)
        bp = MakeBoxPlots(country, unit, out_image, level)
        bp_zeros = MakeBoxPlots(country, unit, out_image_zeros, level, keep_zeros=True)
        bp_log = MakeBoxPlots(country, unit, out_image_log, level, log=True)
        bp_log_zeros = MakeBoxPlots(country, unit, out_image_log_zeros, level, log=True, keep_zeros=True)
        del bp, bp_log, bp_log_zeros
        



if __name__ == "__main__":
    BASEDIR = Path(__file__).resolve().parent.parent
    #countries = ['HTI', 'NAM', 'GHA', 'MOZ', 'NPL']
    countries = ['HTI']
    #levels = ['l1', 'l2']
    levels = ['l2']
    for level in levels:
        for country in countries:
            adm_units = sorted(['_'.join(x.name.split('_')[:3]) for x in BASEDIR.joinpath(f'datain/{country}/2012/04/subnational/{level}').iterdir() if x.name.endswith('.tif')])
            main(country, adm_units, level)
            