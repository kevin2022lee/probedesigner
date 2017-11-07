from django.conf.urls import patterns, include, url
import settings
from django.contrib import admin
from MyBlog.views import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^site_medias/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^html/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.HTML_ROOT }),   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', plaza),
    url(r'^UploadImage',UploadImage),
    url(r'^GetNewestImg',GetNewestImg),
    url(r'^MyBlog/$', index),
    url(r'^MyBlog/register/', register),
    url(r'^MyBlog/reseq/', reseq),
    url(r'^MyBlog/sregister/', sregister),
    url(r'^MyBlog/sreply/', sreply),
    url(r'^MyBlog/classfy/(\d+)/$', show_class),
    url(r'^MyBlog/topics/(\d+)/$',showreply),
    url(r'^MyBlog/login/',alogin),
    url(r'^MyBlog/loginout/',loginout),
    url(r'^MyBlog/search/',search),
    url(r'^MyBlog/oligo/',caloligo),
    url(r'^MyBlog/addseq/',addseq),
    url(r'^MyBlog/showoligo/',showoligo),
    url(r'^MyBlog/userinfo/',userinfo),
    url(r'^MyBlog/checkuser/',checkuser),
    url(r'^MyBlog/checkseq/',checkseq),
    url(r'^MyBlog/modify_userinfo/',modify_userinfo),
    url(r'^MyBlog/addblog/',addblog),
    url(r'^MyBlog/submitblog/',submitblog),
    url(r'^MyBlog/manageblog/',manageblog),
    url(r'^MyBlog/myreplys/',myreply),
    url(r'^MyBlog/myphoto/',myphoto),
    url(r'^MyBlog/checklogin/',checklogin),
    url(r'^MyBlog/edit/(\d+)/',editblogbyid),
    url(r'^MyBlog/delete/',deleteblogbyid),
    url(r'^MyBlog/updateblog/',updateblogbyid),
    url(r'^updatephoto/',updatephotobyid),
    url(r'^MyBlog/updateblogall/',updateblogall),
    url(r'^photo/',showphoto),
    url(r'^zanphoto/(\d+)/$',zanphoto),
    url(r'^book/',book),
    url(r'^book/tag/(\d+)',booktag),
    url(r'^movie/',movie),
    url(r'^Entrez/',Entrez),
    url(r'^downloadentrez/',downloadEntrez),
    #url(r'^MyBlog/',static)
)