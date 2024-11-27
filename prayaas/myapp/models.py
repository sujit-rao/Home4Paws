from django.db import models
import datetime
import os



def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

# Create your models here.
class pet_data(models.Model):
    useremail=models.CharField(max_length=200, blank=True)
    petname=models.CharField(max_length=200)
    pettype=models.CharField(max_length=200)
    petbreed=models.CharField(max_length=200)
    petage=models.IntegerField()
    petgender=models.CharField(max_length=200)
    petdesc=models.CharField(max_length=200)
    petpic=models.ImageField(upload_to=filepath, null=True, blank=True)
    petcity=models.CharField(max_length=200, blank=True)