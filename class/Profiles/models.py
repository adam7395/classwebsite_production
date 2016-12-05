from django.db import models
from django.conf import settings
from allauth.account.signals import user_logged_in, user_signed_up
from django.core.signals import request_finished
from QandA.models import Question, Answer
# Create your models here.

#create a model for a student
class Profile( models.Model):
    firstname = models.CharField(max_length=120, blank=True, null=True)
    lastname = models.CharField(max_length=120, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user = models.OneToOneField( settings.AUTH_USER_MODEL, blank=True, null=True)
    background = models.CharField(max_length=200, blank=True, null=True, default="What is your education level, were you a 109 student, etc.")
    description = models.TextField(blank=True, null=True, default="Where are you from? What is your science background? What do you hope to gain from the class, etc.")
    facepic = models.ImageField( upload_to='pic/', default="pic/scientist.jpg")
    bg_pic = models.ImageField( upload_to='background/', default="background/default_bg.jpg")
    is_staff = models.BooleanField( default=False )

    #the following is for students only
    resume = models.FileField( upload_to='resume/', blank=True, null=True, editable=True),
    #unread_questions = models.ManyToMany(Question)

    '''the following are fields for instructors only'''
    institution = models.CharField(max_length=200, help_text="Where do you work?", blank=True, null=True)
    inst_url = models.URLField(help_text="URL to the homepage of your company", blank=True, null=True)
    protocol = models.CharField(max_length=120, blank=True, null=True, editable=True, choices=[('DNA', 'DNA AGAROSE'), ('pp', 'protein purification'), ('binf', 'bioinformatics') ]   ),

    questions = models.ManyToManyField(Question)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        if self.firstname:
            return self.firstname
        else:
            return self.user.get_username()








def profileCallBack(sender, request, user, **kwargs):
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        profile.email = user.email
        profile.save()




user_signed_up.connect(profileCallBack)
