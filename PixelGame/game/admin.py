from django.contrib import admin
from game.models import Image, Crop, UserProfile, CropOrder

class CropInline(admin.StackedInline):
    model = Crop
    extra = 3

class ImageAdmin(admin.ModelAdmin):
   
    inlines = [CropInline]


admin.site.register(Image, ImageAdmin)
admin.site.register(Crop)
admin.site.register(UserProfile)
admin.site.register(CropOrder)
