#coding:utf-8

# Django imports
from django.http import HttpResponse
from django.views.generic import View
import django.template.context
import django.shortcuts

# Music albums imports
from music_albums import models
from music_albums import common

class Home(View):

    def post(self, request):
        return HttpResponse('result')

    def get(self, request):
        template_variables = {}
        albums = models.Album.objects.all()
        template_variables['albums'] = albums

        template_context =\
            django.template.context.RequestContext(request, template_variables)

        return django.shortcuts.render_to_response(
            common.TEMPLATE__HOME,
            template_context
        )
