import pandas as pd
import shutil
import os
import warnings
import App.utils as utils
import App.mongo_manager as mongo_manager

warnings.filterwarnings('ignore', category=RuntimeWarning)

def launch_etl_official_oils_prices(year_to_load = None, drop_mongo_collections = None):
    print("[INFO] Start launch_etl_official_oils_prices")
    if year_to_load != None and int(year_to_load) < 1985:
        print(f"[WARNING] {year_to_load} 'year_to_load' parameter is < 1985, so data is not available at this date for official_oils_prices")
        return "done"
    if drop_mongo_collections == "true":
        print("[INFO] Drop Mongo collections")
        mongo_manager.drop_mongo_collections(bdd = "datalake", collections= ["official_oils_prices"])
    start_date_to_load, end_date_to_load = utils.determine_dates_to_load_from_mongo(year_to_load, db_name= "datalake", collection= "official_oils_prices")
    df_official_oils_prices = extract_new_official_oils_prices()
    df_official_oils_prices = transform_official_oils_prices(df_official_oils_prices, start_date_to_load, end_date_to_load)
    load_official_oils_prices_to_mongo(df_official_oils_prices)


def extract_new_official_oils_prices():
    print("[INFO] Start extract_new_official_oils_prices")

    # clean working csv folder and recreate it
    if os.path.exists("outputs/official_oils_prices"):
        shutil.rmtree("outputs/official_oils_prices")
    os.makedirs("outputs/official_oils_prices", exist_ok=True)

    # Source = "https://www.ecologie.gouv.fr/politiques-publiques/prix-produits-petroliers" (gouvernemental opendata website)
    url = "https://www.ecologie.gouv.fr/simulator-energies/monitoring/export/59707a7b55c0012d0efade376d62a56d3c86129a"
    df_official_oils_prices = pd.read_excel(url, sheet_name=1, skiprows=0)
    return df_official_oils_prices


def transform_official_oils_prices(df_official_oils_prices, start_date_to_load, end_date_to_load):
    print("[INFO] Start transform_official_oils_prices")

    # rename columns
    df_official_oils_prices = df_official_oils_prices.rename(columns={
        'Gazole €/l ttc': 'official_ttc_GAZOLE_eur_liter',
        'Super sans plomb 95 €/l ttc': 'official_ttc_SP95_eur_liter',
        'Super SP95 - E10 €/l ttc': 'official_ttc_E10_eur_liter',
        'Super sans plomb 98 €/l ttc': 'official_ttc_SP98_eur_liter',
        'Superéthanol E85 €/l ttc': 'official_ttc_E85_eur_liter',
        'GPL €/l ttc': 'official_ttc_GPLC_eur_liter',
    })
    # change dd/mm/yyyy to pandas datetime
    df_official_oils_prices['Date'] = pd.to_datetime(df_official_oils_prices['Date'], dayfirst=True)

    # filter on target date
    start_date_to_load = pd.to_datetime(start_date_to_load)
    end_date_to_load = pd.to_datetime(end_date_to_load)
    df_official_oils_prices = df_official_oils_prices[
        (df_official_oils_prices['Date'] >= start_date_to_load) &
        (df_official_oils_prices['Date'] <= end_date_to_load)
        ]
    print('df_official_oils_prices \n', df_official_oils_prices.head(5))
    return df_official_oils_prices


def load_official_oils_prices_to_mongo(df_official_oils_prices):
    print("[INFO] Start load_official_oils_prices_to_mongo")

    # Save df to csv
    start_year = df_official_oils_prices['Date'].min().year
    end_year = df_official_oils_prices['Date'].max().year
    df_official_oils_prices.to_csv(f"outputs/official_oils_prices/official_oils_prices_{start_year}_{end_year}.csv", index=False)

    # Save df to Mongo
    result = mongo_manager.load_datas_to_mongo(df_official_oils_prices, bdd="datalake",collection="official_oils_prices", index=["Date"])
    if result:
        print(f"correctly loaded official_oils_prices_{start_year}_{end_year} on mongo collection 'official_oils_prices'")

    print(f"END LOAD official_oils_prices_{start_year}_{end_year}")
    return "done"
