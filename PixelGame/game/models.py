from django.db import models
import string
import random
import os
import Image as Im
import logging
from django.contrib.auth.models import User
from datetime import datetime

logger = logging.getLogger(__name__)

def changeName(instance, filename):
    print ("SOMETHING")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (name_generator(), ext)
    print filename
    return os.path.join('croppedImages/', filename)


def name_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Image(models.Model):
    wholeImage = models.ImageField(upload_to = 'wholeImages/')
    level = models.IntegerField(default = 1)
    answer = models.CharField(max_length =200)
    def save(self):
        if not self.id and not self.wholeImage:
            return
        super(Image,self).save()
        image = Im.open(self.wholeImage)
        image=image.resize((500,600),Im.ANTIALIAS)
        image.save(self.wholeImage.path)
        #cropFunction(self)
        # if int(self.level)==1:
        #     for i in range(0,8):
        #         for j in range(0,10):
        #             box = (50*i,50*j,50*(i+1),50*(j+1))
        #             crop = image.crop(box)
        #             holder="something"+self.wholeImage.path.split('.')[-1]
        #             crop.save(holder)
        #             something = Crop(croppedImage=holder,position_x=i,position_y=j)
        #             self.crop_set.add(something)
        #             something.save()

    def __str__(self):              # __unicode__ on Python 2
        return str(self.level)

class Crop(models.Model):
    image = models.ForeignKey(Image)
    croppedImage = models.ImageField(upload_to=changeName)
    position_x = models.IntegerField()
    position_y = models.IntegerField()

    def __str__(self):              # __unicode__ on Python 2
        return str(self.image.answer)+"_"+str(self.position_x)+ str(self.position_y)
 
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    score = models.IntegerField(default=0)
    lastPlayed = models.DateTimeField(default=datetime.now())
    flips = models.IntegerField(default = 3)
    level = models.IntegerField(default = 1)
    cropNumber = models.IntegerField(default = 5)
    hints = models.IntegerField(default = 0)
    letters = models.CharField(max_length = 10000, default = "")
    time_till_flip = models.IntegerField(default =120)
    bestTime = models.CharField(max_length=20000000, default="")
    achievements = models.CharField(max_length=2000000, default ="")

    def __unicode__(self):
        return self.user.username

class CropOrder(models.Model):
    level = models.IntegerField()
    order = models.CommaSeparatedIntegerField(max_length = 1000)

    def __unicode__(self):
        return self.order 




#post_save.connect(cropFunction, sender = Image)
