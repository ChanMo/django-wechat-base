import hashlib
import json
import logging
import os
import time
import urllib.request

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .base import Wechat

logger = logging.getLogger(__name__)


class Wxa(Wechat):
    """
    微信小程序
    """

    def get_pay_data(self, prepay_id):
        " 获取支付数据 "
        data = {
            'appId': self.appid,
            'timeStamp': int(time.time()),
            'nonceStr': self._make_nonce(),
            'package': 'prepay_id='+prepay_id,
            'signType': 'MD5'
        }
        data['paySign'] = self._make_sign(data)

        return data

    def get_qrcode(self, path):
        " 获取小程序二维码 "
        filename = hashlib.md5(path.encode('utf8')).hexdigest().upper()
        qrcode = 'wechat/{}.jpg'.format(filename)

        if default_storage.exists(qrcode):
            return default_storage.url(qrcode)

        token = self._get_access_token()
        url = 'https://api.weixin.qq.com/wxa/getwxacode?access_token={}'.format(token)
        data = {'path': path}
        data = json.dumps(data).encode('utf8')
        with urllib.request.urlopen(url, data) as f:
            res = f.read()
            default_storage.save(qrcode, ContentFile(res))

        return default_storage.url(qrcode)


    def get_delivery(self, delivery_id, waybill_id, order_id, openid=None):
        " 获取物流信息 "
        token = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/express/business/path/get?access_token={}'.format(token)
        data = {
            'order_id': order_id,
            'openid': openid,
            'delivery_id': delivery_id,
            'waybill_id': waybill_id
        }
        data = json.dumps(data).encode('utf8')
        with urllib.request.urlopen(url, data) as f:
            res = f.read().decode('utf8')
            res = json.loads(res)

        return res
