from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question( models.Model ):

    question = models.TextField()
    op = models.ForeignKey( User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)   #the tiem question was asked


    def __str__(self):
        return self.question



class Answer(models.Model):

    response = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    toresponse = models.ForeignKey("Answer", on_delete=models.CASCADE, null=True)
    op = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.response
