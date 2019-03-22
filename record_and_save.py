import sys, os, time, random, string, datetime, requests, ssl
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth

# from functools import wraps
# from flask import request, Response, Flask, redirect, render_template as render

# CONSTANTS

NEXTCLOUD_USER=os.getenv('NEXTCLOUD_USER')
NEXTCLOUD_PASSWORD=os.getenv('NEXTCLOUD_PASSWORD')
NEXTCLOUD_PATH=os.getenv('NEXTCLOUD_PATH')

IMAGE_ROOT_PATH='/home/pi/'

# METHODS
def publish_to_nextcloud(filename_absolute):
    """ Publish a given file (by its absolute filename) to the nextcloud that is specified via envs """
    headers = {"Content-Type" : "image/jpeg"} #, 'Slug': fileName}
    auth = HTTPBasicAuth(NEXTCLOUD_USER, NEXTCLOUD_PASSWORD)
    url = NEXTCLOUD_PATH + filename_absolute.rsplit('/', 1)[-1]
    response = requests.put(url, auth=auth, data=open(filename_absolute, "rb"), headers=headers) 
    return response.status_code

def create_time_string():
    ts = time.time()
    st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
    return st

def create_image_path():
    time_string = create_time_string()
    randstr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    image_name = time_string + '_image_' + randstr + '.jpg'
    image_path = IMAGE_ROOT_PATH+image_name
    return image_path

def record_image():
    image_path = create_image_path()
    os.chdir(IMAGE_ROOT_PATH)
    os.system('fswebcam -r 640x480 -s brightness=1% -S 10 -s Saturation=35% -s Contrast=70% -s Gamma=50% --no-banner '+image_path)
    return image_path

image_path = record_image()
publish_to_nextcloud(image_path)
os.remove(image_path)
#time.sleep(300)
