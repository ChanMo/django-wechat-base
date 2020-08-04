import hashlib
import json
import logging
import os
import time
import urllib.request

from django.conf import settings
from django.core.cache import cache

from .base import Wechat

logger = logging.getLogger(__name__)


class Wxb(Wechat):
    """
    微信服务号
    """
    def __init__(self):
        self.appid = settings.WECHAT['wxb'].get('appid', None)
        self.secret = settings.WECHAT['wxb'].get('secret', None)

    def _make_sign(self, data):
        "生成微信签名"
        data = urllib.parse.urlencode(sorted(data.items()))
        data = urllib.parse.unquote(data)
        data = str.encode(data)

        return hashlib.sha1(data).hexdigest()

    def _get_access_token(self):
        " 获取accesstoken "
        access_token = cache.get('wxb_access_token')

        if access_token:
            return access_token
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(self.appid, self.secret)
        with urllib.request.urlopen(url) as f:
            res = f.read().decode('utf8')
            res = json.loads(res)
            cache.set(
                'wxb_access_token',
                res['access_token'],
                int(res['expires_in'])
            )

            return res['access_token']


    def _get_js_ticket(self):
        ticket = cache.get('wxb_js_ticket')
        if ticket:
            return ticket
        token = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token
        with urllib.request.urlopen(url) as f:
            res = f.read().decode('utf8')
            res = json.loads(res)
        ticket = res['ticket']
        cache.set('wxb_js_ticket', ticket, int(res['expires_in']))
        return ticket


    def get_js_config(self, url, apis=[], debug=False):
        ticket = self._get_js_ticket()
        nonce = self._make_nonce()
        timestamp = int(time.time())
        data = {
            'url': url,
            'noncestr': nonce,
            'jsapi_ticket': ticket,
            'timestamp': timestamp,
        }
        sign = self._make_sign(data)
        config = {
            'debug': debug,
            'appId': self.appid,
            'timestamp': timestamp,
            'nonceStr': nonce,
            'signature': sign,
            'jsApiList': apis,
        }
        return json.dumps(config)
