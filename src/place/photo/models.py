from PIL import Image
from django.contrib import admin
from django.db import models
from django.db.models import permalink
from django.db.models.base import ModelState
from django.db.models.fields.files import ImageFieldFile
from django.db.models.query import QuerySet
from place.photo.utils import _add_thumb
import os

class ThumbnailImageFieldFile(ImageFieldFile):

    def _get_thumb_path(self):
        return _add_thumb(self.path)

    def _get_thumb_url(self):
        return _add_thumb(self.url)

    thumb_path = property(_get_thumb_path)
    thumb_url = property(_get_thumb_url)

    def save(self, name, content, save=True):
        super(ThumbnailImageFieldFile, self).save(name, content, save)
        img = Image.open(self.path)
        img.thumbnail((self.field.thumb_width, self.field.thumb_height), Image.ANTIALIAS)
        img.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super(ThumbnailImageFieldFile, self).delete(save)

class ThumbnailImageField(models.ImageField):

    attr_class = ThumbnailImageFieldFile

    def __init__(self, thumb_width=128, thumb_height=128, *args, **kwargs):
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height
        super(ThumbnailImageField, self).__init__(*args, **kwargs)

class Photo(models.Model):
    post_id = models.CharField(max_length=100)
    caption = models.CharField(max_length=250, blank=True)
    image = ThumbnailImageField(upload_to='photos')

    @classmethod
    def json_default(cls, obj):
        if isinstance(obj, QuerySet):
            return [entity for entity in obj]
        if isinstance(obj, models.Model):
            return obj.to_dict()
        raise TypeError(repr(obj) + ' is not JSON serializable')

    def to_dict(self):
        dict = {}
        for name in self.__dict__.keys():
            column = self.__getattribute__(name)
            if isinstance(column, ImageFieldFile):
                dict['url'] = column.url
                dict['thumb_url'] = column.thumb_url
            elif isinstance(column, ModelState) or name == '_entity_exists':
                continue
            elif name == '_original_pk':
                dict['id'] = column
            else:
                dict[name] = column
        return dict

    @permalink
    def get_absolute_url(self):
        return ('place.photo.views.get', None, {'post_id': self.post_id})

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'image', 'caption')

admin.site.register(Photo, PhotoAdmin)



