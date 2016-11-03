import time
import xmltodict
from .base import Base
from ..models import Message as MessageModel

"""
class Template(Base):
    def push_message(self, data):
        url = self.get_url('message/template/send', {'access_token':self.get_token()})
        message = json.dumps(data)
        result = self.get_data(url, message)
        return result
"""


class Message(Base):
    """
    Message Class, Receive and response message
    """
    def __init__(self):
        pass


    def receive(self, xml):
        receive_data = dict(xmltodict.parse(xml)['xml'])
        return receive_data

    def get_keyword(self, data):
        try:
            msg_type = data['MsgType']

            if msg_type == 'text':
                keyword = data['Content']
            elif msg_type == 'event':
                event = data['Event']
                if event == 'subscribe':
                    keyword = 'subscribe'
                elif event == 'unsubscribe':
                    keyword = 'unsubscribe'
                elif event == 'CLICK':
                    keyword = data['EventKey']
                else:
                    keyword = 'default'
            else:
                keyword = 'default'
        except KeyError:
            keyword = 'default'

        return keyword

    def response(self, keyword, data):
        try:
            message = MessageModel.objects.get(keyword=keyword)
            content = message.content % (
                data['FromUserName'],
                data['ToUserName'],
                int(time.time()),
            )
            return content
        except MessageModel.DoesNotExist:
            return 'success'


"""
class MessageRule(Base):
    def __init__(self, openid):
        super(MessageRule, self).__init__()
        self.message_xml = {
            'xml': {
                'ToUserName': openid,
                'FromUserName': self.appid,
                'CreateTime': '',
                'MsgType': '',
            }
        }
        try:
            self.message_default = settings.WECHAT[0]['message_default']
        except KeyError:
            self.message_default = True

    def get_rule(self, keyword):
        try:
            rule = Rule.objects.get(keyword=keyword)
            return self.response(rule)
        except Rule.DoesNotExist:
            if self.message_default != True:
                result = response_customer_service()
                return result
            else:
                rule = Rule.objects.get(keyword='default')
                return self.response(rule)
        except Rule.DoesNotExist:
            return ""


    def response(self, rule):
        if rule.object_type == 'text':
            result = self.response_text(rule.object_id)
        elif rule.object_type == 'news':
            result = self.response_news(rule.object_id)
        else:
            result = ""
        return result

    def response_text(self, pk):
        text = Text.objects.get(pk=pk)
        message = self.message_xml
        message['xml']['CreateTime'] = int(time.time())
        message['xml']['MsgType'] = 'text'
        message['xml']['Content'] = text.content
        print(message)
        return self.dict_to_xml(message)


    def response_news(self, pk):
        news = News.objects.get(pk=pk)
        message = self.message_xml
        message['xml']['CreateTime'] = int(time.time())
        message['xml']['MsgType'] = 'news'
        message['xml']['ArticleCount'] = 1
        message['xml']['Articles'] = {
            'item': {
                'Title': news.title,
                'Description': news.description,
                'PicUrl': 'http://' + news.pic.url,
                'Url': news.url,
            }
        }
        return self.dict_to_xml(message)


    def response_customer_service(self):
        message = self.message_xml
        message['xml']['CreateTime'] = int(time.time())
        message['xml']['MsgType'] = 'transfer_customer_service'
        return self.dict_to_xml(message)
"""
