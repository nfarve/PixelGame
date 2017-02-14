from django import forms
from game.models import Image

class ImageForm(forms.Form):
    def get_choices():
        possibles = range(1,21)
        choices = list()
        for images in Image.objects.all():
            possibles.remove(images.level)
        for value in possibles:
            choices.append((value,"Level "+str(value)))
        return tuple(choices)
    docfile = forms.ImageField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    CHOICES = get_choices()
    level = forms.ChoiceField(choices=CHOICES, required=True, label='level')
    answer = forms.CharField(max_length=200, label="Image Answer")
    

class CropForm(forms.Form):
    order = forms.CharField(widget=forms.HiddenInput(),label="Order of crops", required=False)
    used = forms.CharField(widget=forms.HiddenInput(),label="Used crops", required=False)
    guess = forms.CharField(max_length = 200, label="What do you think it is?", required=False)
    level= forms.CharField(widget=forms.HiddenInput(),label="level", required=False)
    flips = forms.IntegerField(widget = forms.HiddenInput(), label="flips remaining", required=True)
    points = forms.IntegerField(widget = forms.HiddenInput(), label="Possible Points", required=True)
    score = forms.IntegerField(widget = forms.HiddenInput(), label="Possible Score", required=True)


