from django.contrib import admin

from .models import Label, Album, Artist

admin.site.register(Label)
admin.site.register(Album)
admin.site.register(Artist)
