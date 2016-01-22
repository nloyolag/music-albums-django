from django.http import HttpResponse
from django.views.generic import View

class Home(View):

    def post(self, request):
        return HttpResponse('result')

    def get(self, request):
        return HttpResponse('result')
