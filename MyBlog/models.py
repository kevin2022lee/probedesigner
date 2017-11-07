from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

#class User(models.Model):
    

class BlogUser(models.Model):
    username=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    email_address=models.CharField(max_length=100)
    admin_type=models.BigIntegerField()

class PostType(models.Model):
    typename=models.CharField(max_length=200)
    addtime=models.DateTimeField(auto_now=True)
    
class BlogPost(models.Model):
    u=models.ForeignKey(User,related_name='auth_user_id')
    title = models.CharField(max_length = 150)
    content = models.TextField()
    article_click=models.BigIntegerField()
    artcle_type = models.ForeignKey(PostType,related_name='PostType_id')
    is_recycle = models.BigIntegerField()
    timestamp = models.DateTimeField()

class ReplyPost(models.Model):
    u=models.ForeignKey(BlogPost,related_name='BlogPost_u_id')
    r=models.ForeignKey(BlogPost,related_name='BlogPost_id')
    rcontent=models.TextField(max_length=500)
    createtime = models.DateTimeField(auto_now=True)

class OligoSeqSyt(models.Model):
    uid=models.IntegerField()
    SeqName=models.TextField(max_length=20)
    Sequence=models.TextField(max_length=10000)
    SeqLength=models.IntegerField()
    SeqTm=models.IntegerField()
    SeqAcount=models.IntegerField()
    SeqGcount=models.IntegerField()
    SeqCcount=models.IntegerField()
    SeqTcount=models.IntegerField()
    SeqJcount=models.IntegerField()
    SeqFcount=models.IntegerField()
    SeqGC=models.FloatField()
    SeqMW=models.FloatField()
    SeqOD=models.FloatField()
    SeqText=models.TextField(max_length=1000)
    SeqReverse=models.TextField(max_length=10000)
    SeqAddTime=models.DateTimeField(auto_now=True)

class WebViewCount(models.Model):
    pagename=models.TextField(max_length=20)
    viewcount=models.IntegerField()
    lastviewtime=models.DateTimeField(auto_now=True)

class PhotoDB(models.Model):
    u=models.IntegerField()
    imagename=models.TextField(max_length=50)
    imageurl=models.TextField(max_length=255)
    imagesize=models.TextField(max_length=10)
    zanclick=models.IntegerField()
    uploadtime=models.DateTimeField()
    is_public=models.IntegerField()
    
class userusd(models.Model):
    uuid=models.IntegerField(primary_key=True)
    usd=models.IntegerField()
class DbBook(models.Model):
    bname=models.TextField()
    btype=models.TextField()
    bimage=models.TextField()
    baddr=models.TextField()
    bauthor=models.TextField()
    brnum=models.FloatField()
    bcp=models.TextField()
    bdescription=models.TextField()
class DbMovie(models.Model):
    mname=models.TextField()
    myear=models.TextField()
    mimage=models.TextField()
    mlink=models.TextField()
    mdirecter=models.TextField()
    mrnum=models.FloatField()
    mlist=models.FloatField()
    mnp=models.TextField()
    mdescr=models.TextField()