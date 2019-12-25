import logging
import random

from django.test import TestCase
from wechat.wxa import Wxa

logger = logging.getLogger(__name__)


class QrcodeTest(TestCase):
    def test(self):
        path = '/pages/index/index?promotion=1'
        wxa = Wxa()
        img = wxa.get_qrcode(path)
        self.assertTrue(img)

class DeliveryTest(TestCase):
    " 测试物流信息 "
    def test(self):
        wxa = Wxa()
        order_id = random.randint(1000, 9999)
        delivery_id = 'ZTO'
        waybill_id = ''
        res = wxa.get_delivery(delivery_id, waybill_id, order_id)
        logger.debug(res)
        self.assertEqual(res['delivery_id'], delivery_id)
