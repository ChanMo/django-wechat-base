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
        data = urllib.parse.urlencode({'xml':xml}).encode('utf-8')
        with urllib.request.urlopen(url, data) as f:
            data = f.read()
            return HttpResponse(data)


@csrf_exempt
def index(request):
    data = request.GET
    wx = Message(request)
    try:
        """ First bind """
        echostr = data['echostr']
        result = wx.check_sign(data)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    except KeyError:
        """ Normal message """
        result = wx.response()
        return HttpResponse(result)
