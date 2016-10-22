import sys
import time
import json
import xmltodict
from .base import Base
from ..models import Rule, Text, News

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
        except:
            print("Request data error")
            #sys.exit()
        self.receive_data = data

    def response(self):
        data = self.receive_data
        try:
            msg_type = data['MsgType']
        except KeyError:
            print("message has not msgtype")
            return ""

        rule = MessageRule('test')

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
