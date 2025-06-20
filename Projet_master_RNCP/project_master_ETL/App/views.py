from flask import *
from flask_cors import CORS
from flask_apscheduler import APScheduler
from dotenv import load_dotenv
import os
from datetime import datetime
import logging
import App.lockfile as lockfile
import App.gas_stations_oils_prices as gas_stations_oils_prices

# Load environment variables from the .env file
load_dotenv('env/.env')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
BUCKET_NAME = os.getenv('BUCKET_NAME')

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

@app.route('/etl/launch_complete_pipeline_oil_prices', methods=["POST"])
def api_launch_complete_pipeline_oil_prices():
    lockfile_name = './LOCKFILE_launch_complete_pipeline_oil_prices.lock'
    fd = lockfile.acquire_lock(lockfile_name)
    if fd is None:
        print(f"Job is already running. Skipping execution at {datetime.now()}")
        return {'message': 'Job already running'}, 200
    try:
        year_to_load = request.form.get('year_to_load')
        drop_mongo_collections = request.form.get('drop_mongo_collections')

        gas_stations_oils_prices.launch_etl_gas_stations_oil_prices(year_to_load, drop_mongo_collections)
        return 'ok'
    finally:
        lockfile.release_lock(fd, lockfile_name)


@app.route('/etl/launch_etl_gas_stations_oil_prices', methods=["POST"])
def api_launch_etl_gas_stations_oil_prices():
    lockfile_name = './LOCKFILE_launch_etl_gas_stations_oil_prices.lock'
    fd = lockfile.acquire_lock(lockfile_name)
    if fd is None:
        print(f"Job is already running. Skipping execution at {datetime.now()}")
        return {'message': 'Job already running'}, 200
    try:
        year_to_load = request.form.get('year_to_load')
        drop_mongo_collections = request.form.get('drop_mongo_collections')

        gas_stations_oils_prices.launch_etl_gas_stations_oil_prices(year_to_load, drop_mongo_collections)
        return "ok"
    finally:
        lockfile.release_lock(fd, lockfile_name)
