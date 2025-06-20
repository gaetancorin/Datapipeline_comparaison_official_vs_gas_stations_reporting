import pandas as pd
import App.mongo_manager as mongo_manager

def determine_dates_to_load_from_mongo(year_to_load, bdd, collection):
    if year_to_load:
        # Load only the target year
        print(f"[INFO] year_to_load received: {year_to_load}")
        start_date_to_load = pd.to_datetime(f"{year_to_load}-01-01")
        end_date_to_load = pd.to_datetime(f"{year_to_load}-12-31")
    else:
        print("[INFO] No year_to_load provided, so load only new data")
        last_date_in_datas = mongo_manager.get_last_data_dates_of_one_collection(bdd=bdd, collection=collection)
        if last_date_in_datas != None:
            # Load the next day of the existing row
            start_date_to_load = pd.to_datetime(last_date_in_datas) + pd.Timedelta(days=1)
        else:
            # Load all the datas because not row in collection,
            start_date_to_load = pd.to_datetime("2007-01-01")
        end_date_to_load = pd.Timestamp.today().normalize()
    return start_date_to_load, end_date_to_load