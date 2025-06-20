from flask import *
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime
import time
import logging
# from App.utils import *
import App.utils as utils
import App.lockfile as lockfile
import App.specific_functions as specific_functions

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()


@app.route('/test', methods=["GET"])
def test():
    return {'message': 'this is a test'}

@app.route('/test2', methods=["GET"])
def test2():
    name = specific_functions.get_full_name()
    return {'message': name}

@app.route('/test3', methods=["GET"])
def test3():
    name = "Pierre"
    name_uppercase = utils.change_uppercase(name)
    return {'message': name_uppercase}

@scheduler.task('cron', id='testscheduler',year='*', month='*', day='*', week='*',
                day_of_week='*', hour='*', minute='*', second=0)
@app.route('/test4', methods=["GET"])
def testscheduler():
    lockfile_name = './LOCKFILE_testscheduler.lock'
    fd = lockfile.acquire_lock(lockfile_name)
    if fd is None:
        print(f"Job is already running. Skipping execution at {datetime.now()}")
        return {'message': 'Job already running'}, 200
    try:
        name = "MonsieurScheduler"
        print(name)
        time.sleep(30)
        print("scheduler done")
        return {'message': name}
    finally:
        lockfile.release_lock(fd,lockfile_name)
