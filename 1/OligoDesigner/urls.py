from django.conf.urls import patterns, include, url
from views import index,intro,probedesign,subseq,entrez,fromfile,downloadentrez,entreztoxml,test,x4merCalc,startdesign,NonNshFilter,PostCalcXmer,ProbeSetsXmer,GenerateProbesets
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
    url(r'^downloadentrez', downloadentrez),
    url(r'^xmltoentrez', entreztoxml),
    url(r'^test', test),
    url(r'^x4merCalc', x4merCalc),
    url(r'^startdesign', startdesign),
    url(r'^NonNshFilter', NonNshFilter),
    url(r'^PostCalcXmer', PostCalcXmer),
    url(r'^ProbeSetsXmer',ProbeSetsXmer),
    url(r'^GenerateProbesets',GenerateProbesets),
)
