基于django的微信接口模块
========================

一个基于django的微信接口模块

快速开始:
---------

安装wechat:

.. code-block::

    pip install django-wechat-base

把wechat模块添加到你的settings.py里面:

.. code-block::

    INSTALLED_APPS = (
        ...
        'wechat',
        ...
    )

在settings.py里面添加微信设置信息:

.. code-block::

    # wechat config
    WECHAT_APPID = 'test'
    WECHAT_APPSECRET = 'test'
    WECHAT_TOKEN = 'yourtoken'
    WECHAT_MCH_ID = 'test'
    WECHAT_KEY = 'test'
    WECHAT_JS_DEBUG = 'test'
    WECHAT_JS_APILIST = ['test']


版本更改:
---------
- v1.0 分离基础接口和菜单，回复等功能
- v0.6 添加对python3.x支持
- v0.5 添加客服支持
- v0.4 添加多语言支持
- v0.3 使js配置信息可编辑，添加Qrcode类
- v0.2 添加WxMemberView
- v0.1 第一版
