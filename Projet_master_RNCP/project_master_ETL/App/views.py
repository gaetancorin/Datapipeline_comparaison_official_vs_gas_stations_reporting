from flask import *
from flask_cors import CORS
from flask_apscheduler import APScheduler
from datetime import datetime
import time
import os
import logging
# from App.utils import *
import App.utils as utils
import App.lockfile as lockfile
import App.specific_functions as specific_functions
from dotenv import load_dotenv

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



@app.route('/launch_all_pipeline', methods=["GET"])
def launch_all_pipeline():
    print(AWS_ACCESS_KEY_ID)
    return "ok"
