#coding:utf-8

# Django imports
import django.forms

# Music Albums imports
from music_albums import models
from music_albums import common

class ModelFormAlbum(django.forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ModelFormAlbum, self).__init__(*args, **kwargs)
        self.fields['label'].queryset = models.Label.objects.filter(is_active=True)

    class Meta:
        model = models.Album
        fields = [
            'title',
            'release_date',
            'rating',
            'cover',
            'label'
        ]

        error_messages = {
            'title': {
                'required': common.ERROR__TITLE_REQUIRED
            }
        }
