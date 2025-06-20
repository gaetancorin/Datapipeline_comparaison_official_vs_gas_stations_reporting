from flask import *
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime
import time
import os
import logging
# from App.utils import *
import App.utils as utils
import App.specific_functions as specific_functions

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
CORS(app)
scheduler = APScheduler()

def acquire_lock(lockfile):
    """Acquire a lock on the specified file."""
    try:
        fd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        return fd
    except FileExistsError:
        return None

def release_lock(fd,lockfile):
    """Release the lock."""
    os.close(fd)
    os.remove(lockfile)


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
    lockfile = './FILE_ONLY_FOR_LOCK.lock'
    fd = acquire_lock(lockfile)
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
        release_lock(fd,lockfile)
