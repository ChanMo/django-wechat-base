from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .message import Message

@csrf_exempt
def index(request):
    data = request.GET
    wx = Message(request)
    try:
        echostr = data['echostr']
        result = wx.check_sign(data)
        if result:
            return HttpResponse(echostr)
        else:
            return HttpResponse('error')
    except KeyError:
        result = wx.response()
        return HttpResponse(result)
