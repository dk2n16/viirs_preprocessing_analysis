"""Main module to run zonal stats on all subnational units over all months over the years and per month"""

def main(country):
    print(country)

if __name__ == "__main__":
    #countries = ['HTI', 'NAM', 'NPL', 'MOZ', 'GHA']
    countries = ['HTI']
    for country in countries:
        main(country)