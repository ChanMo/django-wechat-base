import json
import logging
import urllib.request

from .base import Wechat

logger = logging.getLogger(__name__)


class Message(Wechat):
    """
    模板消息
    """
    def send(self, openid, template, data, url=None):
        token = self._get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'.format(token)

        data = {
                "touser":openid,
                "template_id":template,
                "data":data
        }
        data = json.dumps(data).encode('utf8')
        with urllib.request.urlopen(url, data) as f:
            logger.info(f.read().decode('utf8'))
