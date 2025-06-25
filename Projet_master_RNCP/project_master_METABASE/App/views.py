from flask import *
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime
import App.lockfile as lockfile
import time
import os
# import logging
import App.utils as utils

# logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()


@app.route('/is_alive', methods=["GET"])
def api_is_alive():
    print("[INFO] alive")
    return "alive"


@app.route('/save_metabase_db_to_S3', methods=["GET"])
def api_save_metabase_db_to_S3():
    print("[INFO] save_metabase_db_to_S3")
    lockfile_name = './LOCKFILE_save_metabase_db_to_S3.lock'
    fd = lockfile.acquire_lock(lockfile_name)
    if fd is None:
        print(f"Job is already running. Skipping execution at {datetime.now()}")
        return {'message': 'Job already running'}, 200
    try:
        print("do stuffs")
        return "done"
    finally:
        lockfile.release_lock(fd, lockfile_name)

@app.route('/stop_metabase', methods=["GET"])
def api_stop_metabase():
    utils.stop_metabase()
    return "done"

@app.route('/launch_metabase', methods=["GET"])
def api_launch_metabase():
    utils.start_metabase()
    return "done"

@app.route('/delete_metabase_db_in_container', methods=["GET"])
def api_metabase_db_in_container():
    utils.delete_metabase_db_in_container()
    return "done"

@app.route('/copy_metabase_db_from_container', methods=["GET"])
def api_copy_metabase_db_from_container():
    utils.copy_metabase_db_from_container()
    return "done"