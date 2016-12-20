from django.conf.urls import patterns, include, url
from OligoDesigner.views import *
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'OligoDesigner.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^site_medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^probedesign', probedesign),
    url(r'^subseq', subseq),
    url(r'^entrez', entrez),
    url(r'^downloadentrez', downloadentrez),
)
