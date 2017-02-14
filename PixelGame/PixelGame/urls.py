from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PixelGame.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include('game.urls')),
    url(r'^register/', include ('login.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logout/', 'login.views.logout_user'),
    url(r'^login/', 'login.views.user_login'),
    url(r'^getCrop/', 'game.views.getNewCrop'),
    url(r'^getLetters/', 'game.views.getLetters'),
    url(r'^checkGuess/', 'game.views.checkGuess'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
