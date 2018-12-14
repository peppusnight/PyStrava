import requests
import simplejson as js
from datetime import datetime
import pystrava
import numpy as np
import pandas as pd

print('Start!')

download_all_enabled = False

with open('setup.ini') as fid:
    initial_settings = js.load(fid)


stcon = pystrava.strava_user(base_url = 'https://www.strava.com/api/v3',client_id=initial_settings['client_id'],
                                      client_secret=initial_settings['client_secret'],
                                      code=initial_settings['code'])
stcon.get_token()
if download_all_enabled:
    act_list = stcon.get_activity_list()
    with open('activity_list.json','w+') as fid:
        js.dump(act_list,fp=fid)
else:
    with open('activity_list.json','r') as fid:
        act_list = js.load(fp=fid)

act_data = pd.DataFrame(act_list)
act_data['start_date_utc'] = act_data.start_date.apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').timestamp())



a = stcon.get_activity_streams(2006283792)

print('Finish!')

