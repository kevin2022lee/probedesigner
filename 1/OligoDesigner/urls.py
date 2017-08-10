from django.conf.urls import *
from views import *
from django.contrib import admin
import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^site_medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^help/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.HELP_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^probedesign', probedesign),
    url(r'^subseq', subseq),
    url(r'^intro', intro),
    url(r'^entrez', entrez),
    url(r'^fromfile', fromfile),
    url(r'^fromfile_en', fromfile_en),
    url(r'^downloadentrez', downloadentrez),
    url(r'^xmltoentrez', entreztoxml),
    url(r'^xmltoentrez_en', entreztoxml_en),
    url(r'^test', test),
    url(r'^x4merCalc', x4merCalc),
    url(r'^startdesign', startdesign),
    url(r'^startdesign_en', startdesign_en),
    url(r'^NonNshFilter', NonNshFilter),
    url(r'^PostCalcXmer', PostCalcXmer),
    url(r'^ProbeSetsXmer',ProbeSetsXmer),
    url(r'^GenerateProbesets',GenerateProbesets),
)
