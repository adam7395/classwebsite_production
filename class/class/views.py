#class/views.py
from django.shortcuts import render
from announcements.models import Announcement
def index(request):

    #get the announcements
    announce_list = Announcement.objects.order_by('-date')
    print(len(announce_list))

    if request.method == 'POST':
        title = request.POST['title']
        announcement = request.POST['announcement']
        if isinstance( title, str) and isinstance(announcement, str) and len(title) < 100:
            announcement = Announcement.objects.create( title=title, message=announcement)


    announce_list = Announcement.objects.order_by('-date')
    print(len(announce_list))

    return render( request, 'class/index.html', context={"announcements": announce_list})




def about(request):
    return render( request, 'class/about.html')
