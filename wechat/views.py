from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .message import Message

@csrf_exempt
def index(request):
    wx = api.Base()
    data = request.GET
    try:
        echostr = data['echostr']
        result = wx.check_sign(data)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    except KeyError:
        wx_res = api.Response(request)
