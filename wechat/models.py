from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models

class Rule(models.Model):
    keyword = models.CharField(max_length=200)
    object_id = models.IntegerField()
    object_type = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keyword

    def __unicode__(self):
        return self.unicode


class Text(models.Model):
    keyword = models.CharField(_('keyword'), max_length=200)
    content = models.TextField(_('content'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('created'), auto_now=True)

    def __str__(self):
        return self.keyword

    def __unicode__(self):
        return self.keyword

    def clean(self):
        if Rule.objects.filter(keyword=self.keyword).exists():
            raise ValidationError(_('keyword is already exist'))

    def save(self, *args, **kwargs):
        super(Text, self).save(*args, **kwargs)
        Rule.objects.create(
                keyword = self.keyword,
                object_id = self.id,
                object_type = 'text'
        )


class News(models.Model):
    keyword = models.CharField(_('keyword'), max_length=200)
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('created'), auto_now=True)

    def __str__(self):
        return self.keyword

    def __unicode__(self):
        return self.keyword

    def clean(self):
        if Rule.objects.filter(keyword=self.keyword).exists():
            raise ValidationError(_('keyword is already exist'))

    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)
        Rule.objects.create(
                keyword = self.keyword,
                object_id = self.id,
                object_type = 'news'
        )
