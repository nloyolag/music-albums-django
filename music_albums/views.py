#coding:utf-8

# Python imports
import datetime

# Django imports
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages
from django.utils import timezone
import django.template.context
import django.shortcuts

# Music albums imports
from music_albums import models
from music_albums import common
from music_albums import forms


class Home(View):
    form_class = forms.ModelFormAlbum
    template = common.TEMPLATE__HOME

    def post(self, request):
        form = self.form_class(request.POST)
        template_variables = {}

        if form.is_valid():
            album = form.save(commit=False)

            if album.release_date > timezone.now():
                messages.error(
                    request,
                    common.ERROR__FUTURE_ALBUM
                )
            else:
                album.save()
                form.save_m2m()
                form = self.form_class()
                messages.success(
                    request,
                    common.MESSAGE__ALBUM_CORRECTLY_CREATED
                )

        template_variables['form'] = form
        return django.shortcuts.render(
            request,
            self.template,
            template_variables
        )

    def get(self, request):
        template_variables = {}
        albums = models.Album.objects.all()
        template_variables['albums'] = albums
        form = self.form_class()
        template_variables['form'] = form

        return django.shortcuts.render(
            request,
            self.template,
            template_variables
        )
