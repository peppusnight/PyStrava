import requests
import simplejson as js
from datetime import datetime
import pystrava
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

print('Start!')

# Load settings --------------------------------------------------------------------------------------------------------
with open('setup.ini') as fid:
    initial_settings = js.load(fid)
saving_path = initial_settings['saving_path']

# Connect to strava ----------------------------------------------------------------------------------------------------
stcon = pystrava.strava_user(base_url = 'https://www.strava.com/api/v3',client_id=initial_settings['client_id'],
                                      client_secret=initial_settings['client_secret'],
                                      code=initial_settings['code'])
# Get token ------------------------------------------------------------------------------------------------------------
stcon.get_token()

# Download all activity into a JSON ------------------------------------------------------------------------------------
download_all_enabled = False
if download_all_enabled:
    act_list = stcon.get_activity_list()
    with open(saving_path + '/activity_list.json','w+') as fid:
        js.dump(act_list,fp=fid)
else:
    with open(saving_path + '/activity_list.json','r') as fid:
        act_list = js.load(fp=fid)

# Create a DataFrame from the JSON
act_data = pd.DataFrame(act_list)
act_data['start_date_utc'] = act_data.start_date.apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%SZ').timestamp())

# Get activity details -------------------------------------------------------------------------------------------------
act_ids = [2041949158,2006283792,1990887172]
act_streams_dict = stcon.get_activity_streams(act_ids)

# Create dict of DF from activity details
act_streams_dict_df = dict()
for k,v in act_streams_dict.items():
    temp_dict = dict()
    for df_k, df_v in v.items():
        temp_dict[df_k] = df_v['data']

    act_streams_dict_df[k] = pd.DataFrame(temp_dict)

id_sel = str(2041949158)
ax = act_streams_dict_df[id_sel].plot(x='time',y='heartrate',color='C1')
ax.legend(['heartrate'], loc=2)
ax2 = ax.twinx()
act_streams_dict_df[id_sel].plot(x='time',y='altitude',ax=ax2,color='C2')
ax2.legend(['altitude'], loc=1)
ax.grid(True,which='major')
plt.show(block=False)

# Get all preferred segments -------------------------------------------------------------------------------------------
seg_list = stcon.get_starred_segments()
with open(saving_path + '/star_seg_list.json', 'w+') as fid:
    js.dump(seg_list, fp=fid)

print('Finish!')

