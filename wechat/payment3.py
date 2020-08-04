"""
微信支付基础

微信版本: v3
[doc](https://pay.weixin.qq.com/wiki/doc/apiv3/wxpay/pay/transactions/chapter3_2.shtml)

15:48:34 08/06/20
"""

import os
import hmac
import base64
import hashlib
import json
import uuid
import time
import datetime
import random
import logging
import urllib.request
import urllib.error
import subprocess as sp
# from cryptography.hazmat.primitives.ciphers.aead import AESGCM
# from Crypto.PublicKey import RSA
# from Crypto.Hash import SHA256

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .base import Wechat

logger = logging.getLogger(__name__)


class Payment(Wechat):
    def __init__(self):
        self.serial_no= settings.WECHAT['wechat'].get('serial_no', None)


    def get_certificates(self):
        " 获取平台证书, 使用公钥进行验签 "
        url = 'https://api.mch.weixin.qq.com/v3/certificates'

    def _make_sign(self, message):
        " 使用证书进行签名 "
        p1 = sp.Popen(['echo', '-ne', message], stdout=sp.PIPE)
        p2 = sp.Popen(['openssl', 'dgst', '-sha256', '-sign', '_key/apiclient_key.pem'], stdin=p1.stdout, stdout=sp.PIPE)
        p3 = sp.Popen(['openssl', 'base64', '-A'], stdin=p2.stdout, stdout=sp.PIPE)
        return p3.stdout.read().decode()
        # with open("./_key/apiclient_key.pem", "rb") as key_file:
        #     private_key = serialization.load_pem_private_key(
        #         key_file.read(),
        #         password=None,
        #         backend=default_backend()
        #     )

        # signature = private_key.sign(
        #     message.encode('utf8'),
        #     padding.PSS(
        #         mgf=padding.MGF1(hashes.SHA256()),
        #         salt_length=padding.PSS.MAX_LENGTH
        #     ),
        #     hashes.SHA256()
        # )
        # logger.debug(signature)

        # return base64.b64encode(signature).decode()

        #key = RSA.import_key(keyfile)
        #dig = hmac.new(key.encode(), msg=sign_text.encode('utf8'), digestmod=hashlib.sha256).digest()
        #return base64.b64encode(dig).decode()
        # sign_text = sign_text.encode('utf8')
        # hash = SHA256.new()
        # hash.update(pub_key.encode('utf8'))
        # cipher_text = base64.b64encode(hash.digest())
        # return cipher_text.decode('utf8')

    def get_pay_data(self, prepay_id):
        " 获取支付数据 JSAPI "
        data = {
            'appId': self.appid,
            'timeStamp': str(int(time.time())),
            'nonceStr': self._make_nonce(),
            'package': 'prepay_id='+prepay_id,
            'signType': 'RSA'
        }
        logger.debug(data)

        sign = '{}\n{}\n{}\n{}\n'.format(
            data['appId'],
            data['timeStamp'],
            data['nonceStr'],
            'prepay_id='+prepay_id
        )

        data['paySign'] = self._make_sign(sign)

        logger.debug(data)

        return data



    def get_prepay_id(self, data):
        "获取prepayID, JSAPI"
        #out_trade_no = '{:%Y%m%d%H%M%S}{}'.format(datetime.datetime.now(), random.randrange(1000,9999))
        data = {
            'appid': self.appid,
            'mchid': self.mch_id,
            'description': data['description'], # 商品描述
            'out_trade_no': data['out_trade_no'],
            'attach': '', # 自定义数据
            'notify_url': data['notify_url'], # 通知接收地址
            'amount': {
                'total': int(data['total_fee'])
            },
            'payer': {
                'openid': data['openid'], # 支付人
            }
        }
        logger.debug(data)
        jsondata = json.dumps(data)

        nonce_str = str(uuid.uuid4()).replace('-', '')
        timestamp = int(time.time())
        sign = '{}\n{}\n{}\n{}\n{}\n'.format(
            'POST',
            '/v3/pay/transactions/jsapi',
            timestamp,
            nonce_str,
            jsondata,
        )
        logger.debug(sign)

        signature = self._make_sign(sign)
        logger.debug(signature)
        # $ openssl x509 -in apiclient_cert.pem -noout -serial

        url = 'https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi'
        req = urllib.request.Request(url=url, data=jsondata.encode('utf8'))
        authorization = 'WECHATPAY2-SHA256-RSA2048 mchid="{}",nonce_str="{}",signature="{}",timestamp="{}",serial_no="{}"'.format(
            self.mch_id,
            nonce_str,
            signature,
            timestamp,
            self.serial_no
        )
        logger.debug(authorization)
        req.add_header('Content-Type', 'application/json')
        req.add_header('Accept', 'application/json')
        req.add_header('Authorization', authorization)

        try:
            with urllib.request.urlopen(req) as f:
                if f.status == 200:
                    result = f.read().decode('utf8')
                    result = json.loads(result)
                    return result['prepay_id']
        except urllib.error.URLError as e:
            logger.warning('URLError')
            logger.warning(e.code)
            logger.warning(e.reason)
            logger.warning(e.read().decode('utf8'))
        except urllib.error.HTTPError as e:
            logger.warning('HTTPError')
            logger.warning(e.code)
            logger.warning(e.reason)


        return 'test'
        # raise ValueError(result.status)



    def parse_result(self, result):
        " 解析异步通知返回值 "
        try:
            res = json.loads(result)
            res = self._decrypt(
                res['resource']['nonce'],
                res['resource']['ciphertext'],
                res['resource']['associated_data']
            )
            return True, json.loads(res.decode())

        except Exception as e:
            logger.debug(e)
            return False, None

    def _decrypt(self, nonce, ciphertext, associated_data):
        " 解密 "

        key_bytes = str.encode(self.key)
        nonce_bytes = str.encode(nonce)
        ad_bytes = str.encode(associated_data)
        data = base64.b64decode(ciphertext)

        aesgcm = AESGCM(key_bytes)
        return aesgcm.decrypt(nonce_bytes, data, ad_bytes)


    def return_failure(self):
        return json.dumps({'code':'ERROR', 'message':'message'})

    def return_success(self):
        return json.dumps({'code':'SCCESS'})
