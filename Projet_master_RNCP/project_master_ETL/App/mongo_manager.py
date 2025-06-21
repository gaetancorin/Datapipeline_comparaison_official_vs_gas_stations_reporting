import pymongo
import os
from dotenv import load_dotenv
from pymongo import ReplaceOne

load_dotenv('env/.env')
MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_PORT = int(os.getenv('MONGO_PORT'))
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
AUTH_DB = os.getenv('AUTH_DB')

# Setup MongoDB connection (local)
client_mongo = pymongo.MongoClient(
    host=MONGO_HOST,
    port=MONGO_PORT,
    username=MONGO_USER,
    password=MONGO_PASSWORD,
    authSource=AUTH_DB
)

def get_last_data_dates_of_one_collection(db_name, collection):
    db_mongo = client_mongo.get_database(db_name)
    if collection not in db_mongo.list_collection_names():
        print(f"[INFO] Collection '{collection}' not exist in mongo BDD '{db_name}'")
        return None
    collection_mongo = db_mongo.get_collection(collection)
    # Research last date existing in collection
    latest_row = collection_mongo.find_one(
        {"Date": {"$exists": True}},
        sort=[("Date", -1)]
    )
    if latest_row and "Date" in latest_row:
        latest_date = latest_row["Date"]
        print(f"[INFO] Found last date '{latest_date}' into '{collection}' collection")
        return latest_date
    else:
        print(f"[INFO] Not found row with 'Date' inside '{collection}' collection")
        return None

def update_gas_stations_infos(gas_stations_infos, db_name, collection):
    db_mongo = client_mongo.get_database(db_name)
    collection_mongo = db_mongo.get_collection(collection)
    collection_mongo.create_index([("Id_station_essence", pymongo.ASCENDING), ("Cp", pymongo.ASCENDING)])

    # Replace gas_station_infos row only if Id_station_essence matches and row's Last_update is more recent than in Mongo.
    # If no matching Id_station_essence exists, insert the row.
    records = gas_stations_infos.to_dict(orient="records")
    operations = [
        ReplaceOne(
            {
                "Id_station_essence": record["Id_station_essence"],
                "$or": [
                    {"Derniere_maj": {"$lt": record["Derniere_maj"]}},
                    {"Derniere_maj": {"$exists": False}}
                ]
            },
            record,
            upsert=True
        )
        for record in records
    ]
    collection_mongo.bulk_write(operations)
    print("correctly update gas_station_infos datas to MongoDB")


def load_datas_to_mongo(df, bdd, collection, index=None):
    db_mongo = client_mongo.get_database(bdd)
    collection_mongo = db_mongo.get_collection(collection)

    if index != None:
        formated_index = []
        for col in index:
            formated_index.append((col, pymongo.ASCENDING))
        collection_mongo.create_index(formated_index)

    records = df.to_dict(orient="records")
    collection_mongo.insert_many(records)
    return "done"



def drop_mongo_collections(bdd, collections):
    db_mongo = client_mongo.get_database(bdd)
    for collection in collections:
        print(f"[INFO] Into Mongo, drop '{collection.upper()}' collection in '{bdd.upper()}' bdd")
        db_mongo.drop_collection(collection)
