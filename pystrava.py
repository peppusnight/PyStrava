import requests
from datetime import datetime
import simplejson as js
import pandas as pd

class strava_user(object):

    def __init__(self,base_url:str,client_id:str,client_secret:str,code:str):
        '''

        :param base_url:
        :param client_id:
        :param client_secret:
        :param code:
        '''
        self.brl = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.code = code

    def get_token(self)->str:
        '''
        get token
        :return:
        '''

        params = {'grant_type': 'authorization_code',
                  'client_id': self.client_id,
                  'client_secret': self.client_secret,
                  'code': self.code}

        r = requests.post('https://www.strava.com/oauth/token', params=params)
        tkn = js.loads(r.content)['access_token']
        self.token = tkn
        self.std_get_headers = {'Accept': "application/json",
                                'Authorization': "Bearer " + self.token
                                }

        return tkn

    def get_activity_list(self)->list:
        '''

        :return:
        '''
        # List all activities
        url = self.brl + '/activities/'
        querystring = {"before": (round(datetime.now().timestamp())),
                       "after": 0,
                       'page': 0,
                       'per_page': 200}
        headers = self.std_get_headers
        list_completed = False
        idx = 0
        activity_list = []
        while not(list_completed):
            idx +=1
            querystring['page'] = idx
            r = requests.request("GET", url, data='', headers=headers, params=querystring)
            temp_list = js.loads(r.content)
            activity_list = activity_list + temp_list

            if len(temp_list)<200:
                list_completed = True


        return activity_list

    def get_activity_streams(self,actid_list)->list:
        '''

        :param actid_list: 2006283792
        :return:
        '''

        if isinstance(actid_list,(float,int,str)):
            actid_list = [str(actid_list)]

        act_stream_list = []
        for idx, id in enumerate(actid_list):

            url = (self.brl + '/activities/{id}/streams').format(id=id)

            keys_2_get = ['watts','cadence','distance','time','latlng','altitude','velocity_smooth',
                          'heartrate','temp','moving','grade_smooth']
            querystring = {"keys":','.join(keys_2_get),"key_by_type":"true"}

            headers = self.std_get_headers

            r = requests.request("GET", url, data='', headers=headers, params=querystring)

            act_stream_list = act_stream_list + [js.loads(r.content)]

        return act_stream_list

    # def create_df_by(self,by='start_date',activity_list=None)->pd.DataFrame:
    #     '''
    #
    #     :param by:
    #     :param activity_list:
    #     :return:
    #     '''
    #     datetime.strptime(act_list[0]['start_date'], '%Y-%m-%dT%H:%M:%SZ').timestamp()
    #
    #     for i in activity_list:




