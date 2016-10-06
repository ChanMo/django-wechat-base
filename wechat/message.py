import sys
import time
import json
from .base import Base

class Template(Base):
    """
    Push Class
    """
    def push_message(self, data):
        """Push single message"""
        url = self.get_url('message/template/send', {'access_token':self.get_token()})
        message = json.dumps(data)
        result = self.get_data(url, message)
        return result



class Message(Base):
    """
    Message Class, Receive and response message
    """
    def __init__(self, request):
        data = request.body
        try:
            data = dict(xmltodict.parse(data)['xml'])
        except KeyError:
            print("Request data error")
            sys.exit()
        self.receive_data = data

    def response(self):
        data = self.receive_data

        try:
            msg_type = data['MsgType']
        except KeyError:
            print("message has not msgtype")
            return ""

        rule = MessageRule()

        normal_list = ['text','image','voice','video','shortvideo','location',\
                'link','event']

        if msg_type in normal_list:
            try:
                return rule.get_rule(data['Content'])
            except KeyError:
                return ""

        elif msg_type == 'event':
            try:
                return rule.get_rule(data['Event'])
            except KeyError:
                print("msgtype is event, but no event")
                return ""

            event_list = ['SCAN','LOCATION','VIEW']

            if event == 'subscribe':
                "if is subscribe event"
                return rule.get_rule('subscribe')
                """
                try:
                    event_key = data['EventKey']
                except KeyError:
                    pass
                """
            elif event == 'CLICK':
                "if is menu click event"
                try:
                    return rule.get_rule(data['EventKey'])
                except KeyError:
                    print("Click event no eventkey")
                    return ""
            elif event in event_list:
                "if others, return null"
                return ""
            else:
                return ""
        else:
            return ""


class MessageRule(Base):
    def __init__(self, openid):
        self.message_xml = {
            'xml': {
                'ToUserName': self.appid,
                'FromUserName': openid,
                'CreateTime': int(time.time()),
                'MsgType': NULL,
            }
        }

    def get_rule(self, keyword):
        try:
            rule = Rule.objects.get(keyword=keyword)
            return self.response(rule)
        except Rule.DoesNotExist:
            if settings.WECHAT_MESSAGE_DEFAULT_KEFU:
                result = kefu_response()
                return result
            else:
                rule = Rule.objects.get(keyword='default')
                return self.response(rule)
        except Rule.DoesNotExist:
            return ""


    def response(self, rule):
        if rule.type == 'text':
            result = self.response_text(rule.type_id)
        elif rule.type == 'news':
            result = self.response_news(rule.type_id)
        else:
            result = ""
        return result

    def response_text(self, pk):
        text = Text.objects.get(pk=pk)
        message = self.message_xml
        message.CreateTime = int(time.time())
        message.MsgType = 'text'
        return self.dict_to_xml(message)


    def response_news(self, pk):
        news = News.objects.get(pk=pk)
        message = self.message_xml
        message.CreateTime = int(time.time())
        message.MsgType = 'news'
        message.ArticleCount = 1
        message.Articles = {
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
        message.CreateTime = int(time.time())
        message.MsgType = 'transfer_customer_service'
        return self.dict_to_xml(message)
