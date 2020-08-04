# Django Wechat Base

基于django的微信基础模块, 包括使用django缓存, 图片存储等


## Quick Start

Install

```
$ pip install django-wechat-base
```

Update `settings.py`
```
WECHAT = {
    'appid': '',
    'secret': '',
    ...
}
```

Usage

```
from wechat.wxa import Wxa

wxa = Wxa()
qrcode = wxa.get_qrcode('https://github.com/ChanMo/')
print(qrcode)
```

## API List

### Wxa

`from wechat import wxa`

小程序相关功能

* `get_pay_data` 获取小程序支付数据
* `get_qrcode` 获取小程序二维码
* `get_delivery` 获取小程序物流信息

### Wxb

`from wechat import wxb`

公众号模块

* `get_js_config` 获取js配置json

### Message

`from wechat import message`

消息模块

* `send` 发送模块消息

### Payment(v3)

`from wechat import payment3`

微信支付相关(v3)

* `get_pay_data` 获取支付数据
* `parse_result` 解析异步返回值
* `return_failure` 返回错误信息
* `return_success` 返回成功信息

### Payment(v2)

微信支付相关(v2)
