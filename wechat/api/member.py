class Member(Base):
    """
    Member Class
    """

    def get_code_url(self, redirect_uri, state):
        """Get code url"""
        redirect_uri = urllib.quote(redirect_uri, safe='')
        # #becase error sorting...
        # url = 'https://open.weixin.qq.com/connect/oauth2/authorize'
        # param = {
        #     'appid': self.appid,
        #     'redirect_uri': redirect_uri,
        #     'response_type': 'code',
        #     'scope': 'snsapi_userinfo',
        #     'state': state,
        # }
        url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=%s#wechat_redirect' % (self.appid, redirect_uri, state)
        #return self.get_url(url)
        return url

    def get_access_token_url(self, code):
        """Get access token url"""
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
        param = {
            'appid': self.appid,
            'secret': self.appsecret,
            'code': code,
            'grant_type': 'authorization_code'
        }
        url = self.get_url(url, param)
        user = self.get_data(url)
        return user

    def get_user_info(self, code):
        """Get user base info"""
        user = self.get_access_token_url(code)
        url = 'https://api.weixin.qq.com/sns/userinfo'
        param = {
            'access_token': user['access_token'],
            'openid': user['openid'],
            'lang': 'zh_CN',
        }
        url = self.get_url(url, param)
        result = self.get_data(url)
        return result


