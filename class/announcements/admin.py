from django.contrib import admin
from .models import Announcement
# Register your models here.
class LinkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Announcement)
