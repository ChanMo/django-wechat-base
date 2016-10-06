class Pay(Base):
    """
    Pay Class
    """
    mch_id = ''
    key = ''

    def __init__(self):
        super(Pay, self).__init__()
        self.mch_id = settings.WECHAT_MCH_ID
        self.key = settings.WECHAT_KEY


    def set_prepay_id(self, data):
        """Ser prepay id"""
        data['xml'].update({
            'trade_type': 'JSAPI',
            'appid': self.appid,
            'mch_id': self.mch_id,
            'nonce_str': unicode(self.get_random()),
        })
        data['xml']['sign'] = self.get_sign(data['xml'])
        url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        #message = xmltodict.unparse(new_data, pretty=True)
        message = self.dict_to_xml(data)
        result = self.get_data(url, message, False)
        data = dict(xmltodict.parse(result))
        self.prepay_id = data['xml']['prepay_id']


    def get_pay_data(self):
        """Get pay data for html js"""
        data = {
            'appId': self.appid,
            'timeStamp': unicode(int(time.time())),
            'nonceStr': self.get_random(),
            'package': 'prepay_id=%s' % self.prepay_id,
            'signType': 'MD5',
        }
        sign = {'paySign': self.get_sign(data),}
        data.update(sign)
        data = json.dumps(data)
        return data


