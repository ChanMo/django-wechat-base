========
DjangoWechat
========

基于Django的Wechat基础模块, 包括微信开放平台, 微信小程序, 微信公众平台

快速使用
----------

1. 安装`django-wechat`::

    $ pip install django-wechat

2. 更新`settings.py`::

    WECHAT = {
        'appid': '',
        'secret': '',
        'mch_id': '', # 商户号, 支付使用
        'key': '' # 商户key, 支付使用
    }
