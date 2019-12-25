import hashlib
import json
import logging
import random
import string
import urllib.parse
import urllib.request

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class Wechat:
    """
    微信平台(开放平台, 小程序等)
    """
    def __init__(self):
        self.appid = settings.WECHAT.get('appid', None)
        self.secret = settings.WECHAT.get('secret', None)
        self.mch_id = settings.WECHAT.get('mch_id', None)
        self.key = settings.WECHAT.get('key', None)

    def _get_access_token(self):
        " 获取accesstoken "
        access_token = cache.get('wx_access_token')

        if access_token:
            return access_token
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(self.appid, self.secret)
        with urllib.request.urlopen(url) as f:
            res = f.read().decode('utf8')
            res = json.loads(res)
            cache.set(
                'wx_access_token',
                res['access_token'],
                int(res['expires_in'])
            )

            return res['access_token']


    def _make_sign(self, data):
        "生成微信签名"
        data = urllib.parse.urlencode(sorted(data.items()))
        data = urllib.parse.unquote(data)
        data += '&key=' + self.key
        data = str.encode(data)

        return hashlib.md5(data).hexdigest().upper()

    def _make_nonce(self, length=32):
        "生成随即字符串"

        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
