import requests
from datetime import datetime
import simplejson as js

class strava_user(object):

    def __init__(self,base_url,client_id,client_secret,code):
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


    def get_tkn(self)->str:
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
        self.tkn = tkn

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
        headers = {
            'Accept': "application/json",
            'Authorization': "Bearer " + self.tkn,
        }
        list_completed = False
        idx = 0
        activity_list = []
        while not(list_completed):
            idx +=1
            querystring['page'] = idx
            r = requests.request("GET", url, data='', headers=headers, params=querystring)
            temp_list = js.loads(r.content)
            activity_list = activity_list + temp_list

            if len(activity_list)<200:
                list_completed = True

        return activity_list



