from django.db import models

# Create your models here.
# Create your models here.
class Announcement( models.Model ):
    date = models.DateTimeField( auto_now_add=True)
    title = models.CharField(max_length=100, default="Attention")
    message = models.TextField( )



    def __str__(self):
        return  self.message
