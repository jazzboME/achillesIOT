import json
import requests
import logging
from time import strftime as timestamp
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pytz
from datetime import datetime

local_tz = pytz.timezone('America/New_York') # change this to TZ the button is in.

logger = logging.getLogger()

# setup access to Google sheets, using json from Google Cloud Platform
scopes = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scopes=scopes)

logger.setLevel(logging.INFO)
logger.info('Loading function...')

# Time code explanation:
# http://stackoverflow.com/questions/4563272/how-to-convert-a-python-utc-datetime-to-a-local-datetime-using-only-python-stand/13287083#13287083
def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_tz.normalize(local_dt)

def aslocaltimestr(utc_dt):
    return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S')

def addrow(click):
    gc = gspread.authorize(credentials)
    sheet = gc.open('AchillesIoT').worksheet("Sheet1")
    sheet.append_row([aslocaltimestr(datetime.utcnow()), click])   

def lambda_handler(event, context):
    logger.info('got event{}'.format(event))
    addrow(event['clickType']);
    return "OK"

