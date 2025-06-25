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
        utils.extract_metabase_db()
        return "done"
    finally:
        lockfile.release_lock(fd, lockfile_name)
