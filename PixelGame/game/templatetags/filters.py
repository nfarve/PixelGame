from django import template
from game.models import Crop

register = template.Library()

@register.filter(name='get_crop_url')
def get_crop(index):
    print index
    #print Crop.objects.get(id=index).croppedImage.name.split('ImageFolder/')[1]
    return Crop.objects.get(id=index).croppedImage.name.split('ImageFolder/')[1]

@register.filter(name='get_position')
def get_position(index):
    return str(Crop.objects.get(id=index).position_x) + str(Crop.objects.get(id=index).position_y)