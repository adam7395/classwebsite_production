from django.shortcuts import render
from .models import Announcement

# Create your views here.
def AnnouncementView(request):
    announcelist = Announcement.objects.order_by('date')

    return render( request, 'class/index.html', context={'announcements':announcelist})
