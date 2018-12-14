import requests
import simplejson as js
from datetime import datetime
import pystrava

with open('setup.ini') as fid:
    initial_settings = js.load(fid)


strava_session = pystrava.strava_user(base_url = 'https://www.strava.com/api/v3',client_id=initial_settings['client_id'],
                                      client_secret=initial_settings['client_secret'],
                                      code=initial_settings['code'])
