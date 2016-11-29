from django import forms
from .models import Profile



class ProfileForm( forms.ModelForm ):

    class Meta:
        model = Profile
        fields = [ 'firstname', 'lastname', 'background', 'description', 'facepic', 'is_staff',
                        'institution', 'inst_url'  ]
