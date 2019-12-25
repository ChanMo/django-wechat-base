import logging
import urllib.request

import xmltodict

from .base import Wechat

logger = logging.getLogger(__name__)

class Payment(Wechat):
    """
    支付模块
    """
    def get_prepay_id(self, data):
        "获取prepayID"
        data = {
            'xml': {
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': self._make_nonce(),
            'body': data['body'],
            'out_trade_no': data['out_trade_no'],
            'total_fee': data['total_fee'],
            'spbill_create_ip': data['spbill_create_ip'],
            'notify_url': data['notify_url'],
            'openid': data['openid'],
            'trade_type': data['trade_type']
            }
        }
        data['xml']['sign'] = self._make_sign(data['xml'])

        xmldata = xmltodict.unparse(data).encode('utf8')
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        req = urllib.request.Request(url=url, data=xmldata)
        with urllib.request.urlopen(req) as f:
            result = f.read().decode('utf8')
            result = xmltodict.parse(result)

            if result['xml']['return_code'] == 'SUCCESS':
                return result['xml']['prepay_id']

        raise ValueError(result['xml'])



    def parse_result(self, result):
        " 解析异步通知返回值 "
        try:
            xmldata = xmltodict.parse(result)

            if xmldata['xml']['return_code'] == 'SUCCESS':
                is_success = True
            else:
                is_success = False

            return True, xmldata['xml']
        except Exception as e:
            logger.debug(e)

            return False, None


    def return_failure(self):
        return "<xml><return_code><![CDATA[ERROR]]></return_code><return_msg><![CDATA[ERROR]]></return_msg></xml>"

    def return_success(self):
        return "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
