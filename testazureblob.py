from azure.storage.blob import BlockBlobService 
from azure.storage.blob import ContentSettings 
import time, random, os, string, time, sys, datetime

from functools import wraps
from flask import request, Response, Flask, redirect, render_template as render

#app = Flask(__name__)

account_name = os.getenv('AZURE_ACCOUNT_NAME')
account_key = os.getenv('AZURE_ACCOUNT_KEY')
container_name = 'genughabenpi'

#while True:
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
image_name = st + '_image_' + randstr + '.jpg'
image_path = '/home/pi/'+image_name
os.system('fswebcam -r 416x416 --no-banner '+image_path)
block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key) 
block_blob_service.create_blob_from_path( 
  	container_name, 
   	image_name,
        image_path, 
        content_settings=ContentSettings(content_type='image/jpeg')
) 
os.remove(image_path)	
#time.sleep(300)
