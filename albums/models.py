from django.db import models
from PIL import Image
from easy_thumbnails.files import get_thumbnailer

from account.models import Profile
from core.models import TimestampedModelMixin, BaseResource


class Album(TimestampedModelMixin, BaseResource):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(Profile)

    def as_dict(self):
        d = super(Album, self).as_dict()
        return d

def make_square(image, make_square=False, size=None, **kwargs):
    if make_square:
        empty = Image.new("RGBA", size)
        image.thumbnail(size, Image.ANTIALIAS)
        left = (size[0] - image.size[0])/2
        top  = (size[1] - image.size[1])/2
        empty.paste(image, (left, top, image.size[0]+left, image.size[1]+top))
        return empty
    return image

class File(TimestampedModelMixin, BaseResource):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='%Y/%m/%d')
    album = models.ForeignKey(Album)

    def as_dict(self):
        d = super(File, self).as_dict()
        d.update({
            'file': self.file.url,
            'thumbnails': {
                'x-small': get_thumbnailer(self.file)['x-small'].url,
                'small': get_thumbnailer(self.file)['small'].url,
                'medium': get_thumbnailer(self.file)['medium'].url,
                'large': get_thumbnailer(self.file)['large'].url
                }
        })
        return d