from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'created', 'updated')

"""
class RuleAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'object_id', 'object_type', 'created')


class TextAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content', 'created', 'updated')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'created', 'updated')
"""


#admin.site.register(Rule, RuleAdmin)
#admin.site.register(Text, TextAdmin)
#admin.site.register(News, NewsAdmin)
#admin.site.register(Message, MessageAdmin)
