from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm


# Create your views here.
def profile_detail(request, user_id):

    user = User(pk=user_id)
    #get the profile for the user and the fields
    profile = Profile.objects.get(user=user)


    #profile = Profile.objects.get(user=request.user)
    fields = model_to_dict(profile)

    return render( request, 'profiles/profile_detailview.html', {'profile': fields})

def profile_edit(request):

    if request.method == 'POST':
        profile_form = ProfileForm( request.POST, request.FILES, instance=request.user.profile )

        if profile_form.is_valid():

            request.user.is_staff = profile_form.cleaned_data['is_staff']
            
            request.user.save()
            profile_form.save(commit=True)

            fields = model_to_dict( Profile.objects.get( user=request.user))
            user_id = request.user.id
            return redirect( reverse('profile_detail_view', kwargs={'user_id': user_id}))
            #return render( request, 'profiles/profile_detailview.html', {'profile': fields})


    else:
        profile = Profile.objects.get(user=request.user)
        fields = model_to_dict(profile)
        profile_form = ProfileForm( initial=fields )
    return render(request, 'profiles/edit_profile_view.html', {'form':profile_form})


def profile_list(request, list_type=0):

    if list_type == '0':
        profiles = Profile.objects.filter(is_staff=False)
    elif list_type == '1':
        profiles = Profile.objects.filter(is_staff=True)
    else:
        profiles = Profile.objects.all()
    names = [ profile.firstname for profile in profiles]
    images = [ profile.facepic for profile in profiles]
    ids = [ profile.user.id for profile in profiles]
    fields = [ (image, name, i) for image, name, i in zip(images, names, ids)]


    return render( request, 'profiles/list_profile_view.html', {'names': names, 'images': images, 'fields':fields})

'''
class ProfileView(UpdateView):

    model = Profile
    fields = [ 'firstname', 'lastname', 'image', 'education', 'description', 'pic', 'is_staff', 'resume',
                'institution', 'inst_url',  'protocol']
    template_name_suffix = 'profiles/edit_profile.html'
'''
