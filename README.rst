基于django的微信基础功能模块
============================

一个基于django的微信基础功能模块

快速开始:
---------

安装wechat:

.. code-block::

    pip install django-wechat-base


修改settings.py文件:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wechat',
        ...
    )



在settings.py文件底部添加:

.. code-block::

    # wechat config
    WECHAT = [
        {
            'appid': 'demo',
            'appsecret': 'demo',
            'token': 'demo',
        },
    ]


版本更改:
---------
- v1.1 只保留Base基础类
- v1.0 分离基础接口和菜单，回复等功能
- v0.6 添加对python3.x支持
- v0.5 添加客服支持
- v0.4 添加多语言支持
- v0.3 使js配置信息可编辑，添加Qrcode类
- v0.2 添加WxMemberView
- v0.1 第一版
