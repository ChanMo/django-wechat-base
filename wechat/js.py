class Js(Base):
    """
    JsSDK Class
    """

    jsapi = []
    debug = True

    def __init__(self):
        super(Js, self).__init__()
        self.jsapi = settings.WECHAT_JS_APILIST
        self.debug = settings.WECHAT_JS_DEBUG

    def get_ticket(self):
        """Get ticket"""
        jsapi_ticket = cache.get('wx_jsapi_ticket')
        if jsapi_ticket:
            return jsapi_ticket
        else:
            param = {
                'access_token': self.get_token(),
                'type': 'jsapi',
            }
            url = self.get_url('ticket/getticket', param)
            data = self.get_data(url)
            cache.set('wx_jsapi_ticket', data['ticket'], int(data['expires_in']))
            return data['ticket']

    def get_config(self, url):
        """Get config"""
        noncestr = self.get_random()
        timestamp = unicode(int(time.time()))
        sign = self.get_js_sign(url, noncestr, timestamp)
        wx_config = {
            'debug': self.debug,
            'appId': self.appid,
            'timestamp': timestamp,
            'nonceStr': noncestr,
            'signature': sign,
            #'jsApiList': ['onMenuShareTimeline','onMenuShareAppMessage'],
            'jsApiList': self.jsapi,
        }
        return json.dumps(wx_config)


    def get_js_sign(self, url, noncestr, timestamp):
        """Get js sign"""
        data = {
            'url': url,
            'noncestr': noncestr,
            'jsapi_ticket': self.get_ticket(),
            'timestamp': timestamp,
        }
        data = collections.OrderedDict(sorted(data.items()))
        s = ''
        for item in data:
            s = s + item + '=' + data[item] + '&'
        s = s[0:-1]
        s = hashlib.sha1(s).hexdigest()
        return s


