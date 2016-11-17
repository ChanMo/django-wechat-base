from __future__ import unicode_literals
from future.standard_library import install_aliases
install_aliases()

import sys
import hashlib
import json

from urllib.parse import urlencode
from urllib.request import urlopen

from django.core.cache import cache
from django.conf import settings

import xmltodict #pip install xmltodict

class Base(object):
    """
    Wechat Base Class
    appid, appsecret, token in settings.py
    method:
        __init__
        get_token
        get_random
        get_url
        get_data
        get_sign
        check_sign
    """
    base_url = 'https://api.weixin.qq.com/cgi-bin/'
    appid = ''
    appsecret = ''
    token = ''

    def __init__(self):
        try:
            self.appid = settings.WECHAT[0]['appid']
            self.appsecret = settings.WECHAT[0]['appsecret']
            self.token = settings.WECHAT[0]['token']
        except AttributeError:
            print("Base Config is NULL")
            sys.exit()

    def get_token(self):
        """Get wechat access token.Store in cache"""
        access_token = cache.get('wx_access_token')
        if access_token:
            return access_token
        else:
            param = {
                'grant_type': 'client_credential',
                'appid': self.appid,
                'secret': self.appsecret,
            }
            url = self.get_url('token', param)
            data = self.get_data(url)
            cache.set('wx_access_token', data['access_token'],\
                    int(data['expires_in']))
            return data['access_token']


    def get_data(self, url, data='', data_type='json'):
        """Get data from url"""
        #result = urllib.urlopen(url, data)
        #data = data.encode('UTF-8')
        #data = urllib.parse.urlencode(data).encode('utf-8')
        data = data.encode('UTF-8')
        result = urlopen(url, data)
        string = result.read()
        result.close()

        if data_type == 'json':
            result_data = json.loads(string)
        elif data_type == 'string':
            result_data = string

        return result_data


    def get_random(self, length=32):
        """Get random string"""
        result = ''.join(random.choice(string.ascii_lowercase+string.digits)\
                for _ in range(length))
        return result

    def get_sign(self, data):
        """Get sign"""
        data = collections.OrderedDict(sorted(data.items()))
        s = ''
        for item in data:
            s = s + item + '=' + data[item] + '&'
        s = s[0:-1]
        s +=  '&key=%s' % self.key
        s = hashlib.md5(s).hexdigest()
        ss = s.upper()
        return ss

    def check_sign(self, data):
        """Check sign"""
        s = [self.token, data['timestamp'], data['nonce']]
        s.sort()
        ss = ''.join(s)
        new_sign = hashlib.sha1(ss.encode('utf-8')).hexdigest()
        if data['signature'] == new_sign:
            return data['echostr']
        else:
            return False

    def get_url(self, api, param, other=''):
        """make url"""
        url_string = urlencode(param)
        if 'http' in api:
            url = api + '?' + url_string + other
        else:
            url = self.base_url + api + '?' + url_string + other
        return url


    def dict_to_xml(self, data, s=''):
        """trans dict to xml"""
        for key, value in data.iteritems():
            if type(value).__name__ == 'dict':
                s = s + '<' + key + '>' + self.dict_to_xml(value, s) + '</' + key + '>'
            elif type(value).__name__ == 'int':
                s = s + '<' + key + '>' + unicode(value) + '</' + key + '>'
            else:
                s = s + '<' + key + '><![CDATA[' + value + ']]></' + key + '>'
        return s
