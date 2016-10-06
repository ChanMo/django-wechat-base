from django.contrib import admin
from .models import Rule, Text, News

class RuleAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'object_id', 'object_type', 'created')


class TextAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'content', 'created', 'updated')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'created', 'updated')


admin.site.register(Rule, RuleAdmin)
admin.site.register(Text, TextAdmin)
admin.site.register(News, NewsAdmin)
