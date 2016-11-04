import urllib
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .api.base import Base
from .api.message import Message

def simulator(request):
    if request.method == 'GET':
        return render(request, "wechat/simulator.html")
    elif request.method == 'POST':
        url = request.POST['url']
        xml = request.POST['xml']
        """
        data = urllib.parse.urlencode({'xml':xml}).encode('utf-8')
        with urllib.request.urlopen(url, data) as f:
            data = f.read()
            return HttpResponse(data)
        """
        api = Base()
        result = api.get_data(url, xml, 'string')
        return HttpResponse(result)

@csrf_exempt
def index(request):
    try:
        """ First bind """
        echostr = request.GET['echostr']
        wx = Base()
        result = wx.check_sign(request.GET)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    except KeyError:
        """ Normal message """
        wx = Message()
        data = wx.receive(request.body)
        keyword = wx.get_keyword(data)
        #return HttpResponse(keyword)
        result = wx.response(keyword, data)
        return HttpResponse(result)
