from django import forms
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Profile



class ProfileForm( forms.ModelForm ):

    class Meta:
        model = Profile
        fields = [ 'firstname', 'lastname', 'background', 'description', 'facepic', 'is_staff',
                        'institution', 'inst_url',  ]


    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field in self.Meta.fields:
            
            if field == 'institution' or field == 'inst_url':
                self.fields[field].widget.attrs.update({
                    'class': 'instructor-field'
                })
