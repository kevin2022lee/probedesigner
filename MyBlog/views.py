#coding:utf-8
from django.template import RequestContext,loader
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models import Q,connection,Count
from MyBlog.models import BlogPost,ReplyPost,OligoSeqSyt,WebViewCount,User,PhotoDB,PostType,userusd,DbBook,DbMovie
from MyBlog.forms import MsgPostForm
from django.core.paginator import Paginator
from django.core.mail import send_mail  
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import auth
from Bio import Seq,SeqIO,SeqRecord,SeqFeature,Sequencing,SeqUtils,Entrez
from BioSQL import BioSeq,BioSeqDatabase
from MySiteWithPython.settings import EMAIL_HOST_USER 
import time
from datetime import datetime
import sys,urllib
import base64  
import uu
#localip='127.0.0.1:8000'
localip='www.slyyc.asia'
thisyear=time.strftime('%Y',time.localtime(time.time()))

##################################代码开始了！###################################################
@csrf_protect
def static(request):
    return render_to_response('blog/index.htm',context_instance=RequestContext(request))
@csrf_protect
def index(request):
    posts = BlogPost.objects.filter(is_recycle=0).order_by('-timestamp')
    pagesize = int(request.GET.get('ps', '20'))
    paginator = Paginator(posts,pagesize)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    posts = paginator.page(page).object_list #取paginator对象的当前页记录内容
    hots=BlogPost.objects.filter(is_recycle=0).order_by('-timestamp')[:15]
    types=PostType.objects.all
    replys=User.objects.raw(
                            u'SELECT MyBlog_replypost.id,MyBlog_replypost.r_id,auth_user.username,MyBlog_replypost.rcontent,MyBlog_replypost.createtime,MyBlog_replypost.u_id FROM auth_user LEFT JOIN MyBlog_replypost ON MyBlog_replypost.u_id = auth_user.id LEFT JOIN MyBlog_blogpost ON MyBlog_blogpost.id = MyBlog_replypost.r_id WHERE is_superuser = 0 AND is_recycle = 0 ORDER BY MyBlog_replypost.createtime DESC LIMIT 0,15'
                            )
    current = paginator.page(page)
    global localip
    count=getcount(1)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
            page_numbers=range(page-4,page+4)                
    return render_to_response('archive.html',{'types': types,
                                              'posts': posts,
                                              'hots':hots,
                                              'replys':replys,
                                              'is_paginated': paginator.num_pages > 1,#是否分页
                                              'has_next': current.has_next(),
                                              'has_previous': current.has_previous(),
                                              'current_page': page,
                                              'next_page': page + 1,
                                              'previous_page': page - 1,
                                              'pages': paginator.num_pages,
                                              'page_numbers': page_numbers,
                                              'pagesize':pagesize,
                                              'hits' : paginator.count,
                                              'localip':localip,
                                              'thisyear':thisyear,
                                              'count':count,
                                              },context_instance=RequestContext(request))
    ####################################博客首页实现代码#############################
def register(request):
    global localip
    count=getcount(10)
    return render_to_response('register.html',{'localip':localip,'thisyear':thisyear,'count':count,},context_instance=RequestContext(request))
@csrf_protect
def sreply(request):
    if request.method == 'POST':
        r_id = request.GET.get('bid') 
        form = MsgPostForm(request.POST) 
        if form.is_valid() :             
            p = ReplyPost(
                             r_id  = int(r_id) ,
                             u_id  = int(request.session.get('uid')) ,                              
                             rcontent = request.POST['rcontent'],                             
                             )             
            p.save()  
            updateusd(int(request.session.get('uid')),3)
            addusd=userusd.objects.get(uuid=int(request.session.get('uid')))
            request.session['usd']=addusd.usd
            return HttpResponseRedirect('../topics/'+r_id+'/')         
        else:             
            return HttpResponse('error!')     
##########################提交回复功能实现代码##########################################
@csrf_protect
def showreply(request,rid):
        global localip
        count=getcount(3)
        click=getclick(rid)
        select={'day':connection.ops.date_trunc_sql('day','timestamp')}
        start_date='2014-1-1 0:0:0'
        end_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        cds=BlogPost.objects.filter(timestamp__range=(start_date, end_date)).extra(select={'year': "EXTRACT(year FROM timestamp)",
                                              'month': "EXTRACT(month from timestamp)"}
                                      ).values('year', 'month').annotate(number=Count('id')).order_by('-timestamp')[:20]
        posts=BlogPost.objects.raw(u'SELECT a.*,b.username,c.typename FROM (MyBlog_blogpost AS a LEFT JOIN auth_user AS b ON a.u_id = b.id) LEFT JOIN MyBlog_posttype AS c ON a.artcle_type_id = c.id WHERE a.id ='+str(rid))
        types=PostType.objects.all
        for p in posts:
            title=p.title
        rposts=ReplyPost.objects.raw(u'select a.*,b.username from MyBlog_replypost as a left join auth_user as b on a.u_id=b.id where r_id='+str(rid)) 
        replys=len(list(rposts))
        return render_to_response('show.html',{
                                               'types':types,
                                               'cds':cds,
                                               'title':title,
                                               'count':count,
                                               'posts': posts,
                                               'rposts':rposts,
                                               'localip':localip,
                                               'thisyear':thisyear,
                                               'click':click,
                                               'replys':replys
                                               },context_instance=RequestContext(request))
##########################显示主题回复功能实现代码##########################################
@csrf_exempt   
###################################################################################
def show_class(request,tid):
    global localip
    types=PostType.objects.all
    start_date='2010-1-1 0:0:0'
    end_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    cds=BlogPost.objects.filter(timestamp__range=(start_date, end_date)).extra(select={'year': "EXTRACT(year FROM timestamp)",
                                              'month': "EXTRACT(month from timestamp)"}
                                      ).values('year', 'month').annotate(number=Count('id')).order_by('-timestamp')[:20]
    crs=BlogPost.objects.filter(artcle_type=tid).order_by('-timestamp')
    pagesize = int(request.GET.get('ps', '40'))
    paginator = Paginator(crs,pagesize)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    crs = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)  
    return render_to_response('show_class.html',{'types':types,
                                                 'crs':crs,
                                                 'cds':cds,
                                                 'is_paginated': paginator.num_pages > 1,#是否分页
                                                 'has_next': current.has_next(),
                                                 'has_previous': current.has_previous(),
                                                 'current_page': page,
                                                 'next_page': page + 1,
                                                 'previous_page': page - 1,
                                                 'pages': paginator.num_pages,
                                                 'page_numbers': page_numbers,
                                                 'pagesize':pagesize,
                                                 'hits' : paginator.count,
                                                  'localip':localip,
                                                 },context_instance=RequestContext(request)) 
    
#########################################################################################
@csrf_protect
def alogin(request): 
    global localip 
    errors= []  
    account=None  
    password=None  
    if request.method == 'POST' :  
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/') 
        account = request.POST['account']  
        password= request.POST['password']  
        if account is not None and password is not None :
            user = auth.authenticate(username=account,password=password)
            if user:
                    auth.login(request,user)
                    request.session['is_logined']=True
                    request.session['nick']=account
                    users=User.objects.get_by_natural_key(username=account)
                    request.session['uid']=users.id
                    request.session['email']=users.email  
                    request.session['lastlogin']=users.last_login.strftime('%y-%m-%d %H:%M:%S')
                    updateusd(int(users.id),1)
                    usds=userusd.objects.get(uuid=int(users.id))
                    request.session['usd']=usds.usd
                    return HttpResponseRedirect('http://'+localip+'/MyBlog/' )
            else:
                errors='<script type="text/JavaScript">alert("对不起！密码错误。你丫是不是忘记密码了？");window.location.href=document.referrer;</script>'                        
                return HttpResponse(errors)

##########################博客登陆功能实现代码##########################################
def loginout(request):
    auth.logout(request)
    return HttpResponseRedirect('../') 
##########################博客注销功能实现代码##########################################
def sregister(request): 
    errors= []  
    account=None  
    password=None  
    password2=None  
    email=None  
    CompareFlag=False  
  
    if request.method == 'POST':  
        if not request.POST.get('account'):  
            errors.append('请输入账户')  
        else:  
            account = request.POST.get('account')  
        if not request.POST.get('password'):  
            errors.append('请输入密码')  
        else:  
            password= request.POST.get('password')  
        if not request.POST.get('password2'):  
            errors.append('请确认密码')  
        else:  
            password2= request.POST.get('password2')  
        if not request.POST.get('email'):  
            errors.append('请输入邮箱')  
        else:  
            email= request.POST.get('email')  
  
        if password is not None and password2 is not None:  
            if password == password2:  
                CompareFlag = True  
            else :  
                errors.append('两次密码不一致 ')  
############################################################################  
##############################################################################  
        if account is not None and password is not None and password2 is not None and email is not None and CompareFlag :  
            uuidmax=User.objects.count()
            usdinsert=userusd(
                              uuid=uuidmax+1,
                              usd=0,
                              )
            usdinsert.save()
            user=User.objects.create_user(account,email,password)  
            user.is_active=True  
            user.save
#发送确认邮件代码            
            subject = u'NO-REPLY:欢迎会到我的大学汇之坤坤大神部落格'
            html_content = loader.render_to_string('mail.html',{
                                                                'account':account,
                                                                'email':email,
                                                                'password':password,
                                                                })
            msg = EmailMessage(subject, html_content, EMAIL_HOST_USER, [email])
            msg.content_subtype = "html" # Main content is now text/html
            msg.send()
            #title='No-Reply<B>欢迎注册坤坤大神的部落格</B>'  
            #message=u'<p>欢迎注册坤坤大神的部落格</p><br/><p>请牢记你的用户名为</p><br/><p>注册邮箱为 <a>@</a>,如果遗忘密码可以通过此邮箱找回！</p>'   
            #mail_list=[email]  
            #send_mail(subject=title,message=message,from_email=EMAIL_HOST_USER,recipient_list=mail_list,fail_silently=False,connection=None)    
            return HttpResponseRedirect('../')  
##########################用户注册能实现代码##########################################
def checkuser(request):
    if request.method== 'GET':
        user = request.GET.get('username').encode('UTF-8')
        check_results=User.objects.filter(username__iexact=user)
        count_user = len(list(check_results))
        if count_user == 1:
            result = 'registered'
        else:
            result= 'null'
        return HttpResponse(result)
##########################验证图片的实现代码##########################################

@csrf_exempt
def search(request):
    search_words=request.POST.get('search_words')
    global localip
    count=getcount(4)
    search_results=BlogPost.objects.filter(Q(title__icontains=search_words),Q(is_recycle=0))
    movie_results=DbMovie.objects.filter(Q(mname__icontains=search_words))
    book_results=DbBook.objects.filter(Q(bname__icontains=search_words))
    result_count=len(list(search_results))
    movie_count=len(movie_results)
    book_count=len(book_results)
    return render_to_response('search.html',{
                                             'count':count,
                                             'movie_count':movie_count,
                                             'book_count':book_count,
                                             'results':search_results,
                                             'mresults':movie_results,
                                             'bresults':book_results,
                                             'search_words':search_words,
                                             'localip':localip,
                                             'thisyear':thisyear,
                                             'result_count':result_count,
                                             },context_instance=RequestContext(request))
####################################关键字检索模块# ##################################
def caloligo(request): 
    global localip  
    count=getcount(7)
    return render_to_response('caloligo.html',{'count':count,'localip':localip,'thisyear':thisyear,},context_instance=RequestContext(request))
#################################添加序列代码#############################################################
@csrf_protect
def addseq(request):
    if request.method == 'POST':           
            s = OligoSeqSyt(
                             uid = int(request.session.get('uid')) ,
                             SeqName  = request.POST['oligonameBox'] ,                              
                             Sequence = request.POST['oligoBox'],  
                             SeqLength = request.POST['lBox'],
                             SeqTm = request.POST['tmBox'],
                             SeqAcount = request.POST['AcountBox'],
                             SeqGcount = request.POST['GcountBox'],
                             SeqCcount = request.POST['CcountBox'],
                             SeqTcount = request.POST['TcountBox'],
                             SeqJcount = request.POST['JcountBox'],
                             SeqFcount = request.POST['FcountBox'],
                             SeqGC = request.POST['gcBox'],
                             SeqMW = request.POST['mwBox'],
                             SeqOD = request.POST['odBox'],  
                             SeqText=request.POST['TextBox'], 
                             SeqReverse=request.POST['oligoreverse'],                         
                             )             
            s.save()             
            return HttpResponseRedirect('../oligo/')           
######################################################################################################
def checkseq(request):
    if request.method=='GET':
        u=request.session.get('uid')
        seq=str(request.GET.get('sequence'))
        check_seq=OligoSeqSyt.objects.filter(Q(Sequence=seq),Q(uid=u))
        count_seq=len(list(check_seq))
        if count_seq>=1:
            result='submited'
        else:
            result='null'
        return HttpResponse(result)
#######################################################################################################
###############################核酸互补实现代码###################################################################
def reseq(request):
    if request.method=='GET':
        seqs=str(request.GET.get('sequence'))
        re_seq=''
        for s in seqs:
            if s=='A':
                re_s='T'
                re_seq=re_seq+re_s
            elif s=='T':
                re_s='A'
                re_seq=re_seq+re_s
            elif s=='G':
                re_s='C'
                re_seq=re_seq+re_s
            elif s=='C':
                re_s='G'
                re_seq=re_seq+re_s
            elif s=='J':
                re_s='F'
                re_seq=re_seq+re_s
            elif s=='F':
                re_s='J'
                re_seq=re_seq+re_s
            else:
                re_s='^'
                re_seq=re_seq+re_s
        return HttpResponse(re_seq[::-1])
#######################################################################################################
def userinfo(request):
    global localip
    count=getcount(2)
    u=request.session['uid']
    show_user=User.objects.get(id=u) 
    return render_to_response('userinfo.html',{'count':count,'localip':localip,'thisyear':thisyear,'show_user':show_user},context_instance=RequestContext(request))
#######################################################################################################
def showoligo(request):
    u=request.session.get('uid')
    oligos=OligoSeqSyt.objects.filter(uid=u)
    global localip 
    count=getcount(5)
    return render_to_response('showoligo.html',{'count':count,'localip':localip,'oligos':oligos},context_instance=RequestContext(request))
def modify_userinfo(request):
    if request.method=='POST':
        u=request.session.get('uid')
        modify_user=User.objects.get(id=u)
        modify_user.first_name=request.POST['FamilyName'].encode('UTF-8')
        modify_user.last_name=request.POST['LastName'].encode('UTF-8')
        modify_user.save()
    return HttpResponseRedirect('../userinfo/') 
####################################发表博客代码####################################################
def addblog(request):
    global localip
    count=getcount(6)
    types=PostType.objects.all
    return render_to_response('useraddblog.html',{'count':count,'types':types,'localip':localip,},context_instance=RequestContext(request))
def submitblog(request):
    if request.method=='POST':
        u_id=int(request.session.get('uid'))
        title=request.POST['articletitle']
        content=request.POST['articlecontent'].encode('UTF-8')
        typeid=int(request.POST['articletype'])
        b=BlogPost(
                   u_id=u_id,
                   title=title,
                   content=content,
                   article_click=0,
                   artcle_type_id=typeid,
                   is_recycle=0,
                   timestamp=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                   )
        b.save()
        updateusd(int(u_id),5)
        addusd=userusd.objects.get(uuid=int(u_id))
        request.session['usd']=addusd.usd
        return HttpResponseRedirect('../') 
##########################################站点计数器##################################################
def getcount(pid):     
    viewcounts=WebViewCount.objects.get(id=pid)
    countnow=int(viewcounts.viewcount)  
    try:
        viewcountupdate = WebViewCount.objects.get(id=pid)
        viewcountupdate.viewcount=countnow+1
        viewcountupdate.save()
        counts=WebViewCount.objects.get(id=pid)
        count=counts.viewcount
    except:
        count=countnow
    return count
###########################################文章点击率代码################################################
def getclick(articleid):
    articleclicks=BlogPost.objects.get(id=articleid)
    clicknow=int(articleclicks.article_click)
    try:
        articleclickupdate=BlogPost.objects.get(id=articleid)
        articleclickupdate.article_click=clicknow+1
        articleclickupdate.save()
        clicks=BlogPost.objects.get(id=articleid)
        click=clicks.article_click
    except:
        click=clicknow
    return click
###################管理博客代码######################################################################
def manageblog(request):
    u=request.session.get('uid')
    global localip
    count=getcount(8)
    if request.GET.get('listtype')=='recycle':
        mposts=BlogPost.objects.filter(Q(u_id=u),Q(is_recycle=1)).order_by('-timestamp')
        pagesize = int(request.GET.get('ps', '20'))
        paginator = Paginator(mposts,pagesize)#使用paginator对象
        page = int(request.GET.get('p', '1'))#取当前页的号码
        mposts = paginator.page(page).object_list #取paginator对象的当前页记录内容
        current = paginator.page(page)
        if page <= 5 and page<=paginator.num_pages-4:
            page_numbers=range(1,7)
        elif page <= 5 and page>paginator.num_pages-4:
            page_numbers=range(1,paginator.num_pages+1)
        elif (page > 5) and ( page >= paginator.num_pages - 4):
            page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
        elif (page > 5) and (  page <= paginator.num_pages - 4):
            page_numbers=range(page-4,page+4) 
    else:
        mposts=BlogPost.objects.filter(Q(u_id=u),Q(is_recycle=0)).order_by('-timestamp')  
        pagesize = int(request.GET.get('ps', '20'))
        paginator = Paginator(mposts,pagesize)#使用paginator对象
        page = int(request.GET.get('p', '1'))#取当前页的号码
        mposts = paginator.page(page).object_list #取paginator对象的当前页记录内容
        current = paginator.page(page)
        if page <= 5 and page<=paginator.num_pages-4:
            page_numbers=range(1,7)
        elif page <= 5 and page>paginator.num_pages-4:
            page_numbers=range(1,paginator.num_pages+1)
        elif (page > 5) and ( page >= paginator.num_pages - 4):
            page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
        elif (page > 5) and (  page <= paginator.num_pages - 4):
            page_numbers=range(page-4,page+4)      
    return render_to_response('manageblog.html',{
                                                'mposts':mposts,
                                                'count':count,
                                                'localip':localip,
                                                'thisyear':thisyear,
                                                'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':20,
                                                'hits' : paginator.count,
                                                'type': request.GET.get('listtype')
                                                },context_instance=RequestContext(request))
###################################我的回复代码####################################################
def myreply(request):
    u=request.session.get('uid')
    global localip
    mrs=BlogPost.objects.raw(
                     u'SELECT MyBlog_replypost.id,MyBlog_blogpost.title,username,typename,createtime,MyBlog_replypost.u_id,MyBlog_blogpost.id as bid from MyBlog_blogpost LEFT JOIN auth_user on MyBlog_blogpost.u_id=auth_user.id LEFT JOIN MyBlog_posttype on MyBlog_blogpost.artcle_type_id=MyBlog_posttype.id LEFT JOIN MyBlog_replypost ON MyBlog_blogpost.id=MyBlog_replypost.r_id where MyBlog_replypost.u_id='+str(u)
                     )
    pagesize = int(request.GET.get('ps', '25'))
    paginator = Paginator(list(mrs),pagesize)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    mrs = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-5,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)   
    return render_to_response('myreplys.html',{
                                               'mrs':mrs,
                                               'localip':localip,
                                               'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':pagesize,
                                                'hits' : paginator.count,
                                               },context_instance=RequestContext(request))
############################我的图片代码#########################################################################
def myphoto(request):
    global localip
    u=request.session.get('uid')
    if request.GET.get('listtype')=='private':
        photos=PhotoDB.objects.filter(Q(u=u),Q(is_public=1)).order_by('-uploadtime')
        pagesize = int(request.GET.get('ps', '6'))
        paginator = Paginator(photos,pagesize)#使用paginator对象
        page = int(request.GET.get('p', '1'))#取当前页的号码
        photos = paginator.page(page).object_list #取paginator对象的当前页记录内容
        current = paginator.page(page)
        if page <= 5 and page<=paginator.num_pages-4:
            page_numbers=range(1,7)
        elif page <= 5 and page>paginator.num_pages-4:
            page_numbers=range(1,paginator.num_pages+1)
        elif (page > 5) and ( page >= paginator.num_pages - 4):
            page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
        elif (page > 5) and (  page <= paginator.num_pages - 4):
            page_numbers=range(page-4,page+4) 
    else:
        photos=PhotoDB.objects.filter(Q(u=u),Q(is_public=0)).order_by('-uploadtime') 
        pagesize = int(request.GET.get('ps', '6'))
        paginator = Paginator(photos,pagesize)#使用paginator对象
        page = int(request.GET.get('p', '1'))#取当前页的号码
        photos = paginator.page(page).object_list #取paginator对象的当前页记录内容
        current = paginator.page(page)
        if page <= 5 and page<=paginator.num_pages-4:
            page_numbers=range(1,7)
        elif page <= 5 and page>paginator.num_pages-4:
            page_numbers=range(1,paginator.num_pages+1)
        elif (page > 5) and ( page >= paginator.num_pages - 4):
            page_numbers=range(paginator.num_pages-6,paginator.num_pages+1)
        elif (page > 5) and (  page <= paginator.num_pages - 4):
            page_numbers=range(page-4,page+4)    
    return render_to_response('userphoto.html',{
                                                'photos':photos,
                                                'localip':localip,
                                                'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':6,
                                                'hits' : paginator.count,
                                                'type': request.GET.get('listtype'),
                                                },context_instance=RequestContext(request))
##################################删除博客代码##################################################################
def deleteblogbyid(request):
    id=request.GET.get('id')
    delete=BlogPost.objects.get(id=id)
    delete.delete()
    tips='<script type="text/JavaScript">alert("删除成功！");window.location.href=document.referrer;</script>' 
    return HttpResponse(tips)
####################################编辑博客代码####################################################
def editblogbyid(request,id):
        global localip
        count=getcount(9)
        blogedits=BlogPost.objects.filter(id=id)
        types=PostType.objects.all
        return render_to_response('editblog.html',{'blogedits':blogedits,'types':types,'count':count,'localip':localip,'thisyear':thisyear,},context_instance=RequestContext(request))
####################################更新blog的状态########################################################
def updateblogbyid(request):
    if 'checkid' in request.GET and request.GET['checkid']:
        ids = request.GET.getlist('checkid',[])
        for id in ids:
            ub=BlogPost.objects.get(id=int(id))
            if ub.is_recycle==0:
                ub.is_recycle=1
                ub.save()
            else:
                ub.is_recycle=0
                ub.save()            
    return HttpResponseRedirect('../manageblog/') 
###############################更新个人积分#########################################################
def updateusd(id,jf):
    if id<>'':
        au=userusd.objects.get(uuid=id)
        au.usd=au.usd+int(jf)
        au.save()
#########################编辑部落格######################################################################
def updateblogall(request):
    if request.method=='POST':
        id=request.POST['bid']
        eb=BlogPost.objects.get(id=id)
        eb.title=request.POST['articletitle']
        eb.content=request.POST['articlecontent']
        eb.artcle_type_id=int(request.POST['articletype'])
        eb.save()
    return HttpResponseRedirect('../manageblog/') 
##################################检查登录状态代码##################################################
def checklogin(request):
    loginstatus=request.session.get('is_logined')
    return HttpResponse(loginstatus)
#########################################大神部落广场源代码#########################################
def plaza(request):
    global localip
    count=getcount(11)
    pics=PhotoDB.objects.raw(
                             'SELECT auth_user.id,imagename,username,imageurl,imagesize FROM MyBlog_photodb LEFT JOIN auth_user ON MyBlog_photodb.u=auth_user.id where MyBlog_photodb.is_public=0 ORDER BY MyBlog_photodb.uploadtime DESC LIMIT 0,4'
                             )
    firsts=BlogPost.objects.filter(is_recycle=0).order_by('-timestamp')[0:1]
    plazas=BlogPost.objects.filter(is_recycle=0).order_by('-timestamp')[1:10]
    hotarticles=BlogPost.objects.filter(is_recycle=0).order_by('-article_click')[:3]
    return render_to_response('plaza.html',{'count':count,'hotarticles':hotarticles,'pics':pics,'localip':localip,'thisyear':thisyear,'firsts':firsts,'plazas':plazas,},context_instance=RequestContext(request))
#########################图片上传源代码#############################################################
@csrf_protect
def UploadImage(request): 
    if request.method == 'POST':  
        content = request.FILES['ImageField']#picfile要和html里面一致
         
    from os import environ  
    online = environ.get("APP_NAME", "")   
   
    if online:  
        import sae.const  
        access_key = sae.const.ACCESS_KEY  
        secret_key = sae.const.SECRET_KEY  
        appname = sae.const.APP_NAME  
        domain_name = "img2"  #刚申请的domain         
           
        import sae.storage
        s = sae.storage.Client()  
        ob = sae.storage.Object(content.read())
        cname=content.name
        cname_rb=base64.encodestring(datetime.now().strftime("%Y%m%d%H%M%S%f")+'_'+str(len(cname)))[:-3]+'.'+cname.split('.')[-1]
        imageurl = s.put(domain_name, cname_rb, ob) 
        image = PhotoDB(
                    u=request.session.get('uid'),
                    imagename=cname,
                    imageurl=imageurl,
                    imagesize=content.size/1024,
#                    uploadtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    zanclick=1,
                    is_public=0,
                    )             
        image.save()    
        return HttpResponse(imageurl)
    return HttpResponse("error!")
###############################异步获取最新的图片地址###############################
def GetNewestImg(request):
    if request.method=="GET":
        pics=PhotoDB.objects.filter(Q(u=request.session.get('uid')),Q(is_public=0)).order_by('-uploadtime')[0:1]
        if pics:
            for pic in pics:
                return HttpResponse(pic.imageurl)
        else:
            return HttpResponse('http://kkds1314-upload.stor.sinaapp.com/nophoto_420x300.jpg')
#####################################豆瓣api接口######################################
def book(request):
    global localip
    tag=request.GET.get('tag','top250')
    books=DbBook.objects.filter(Q(btype__contains=tag))
    paginator = Paginator(books,25)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    books = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-5,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)   
    return render_to_response('douban.html',{
                                             'tag':tag,
                                             'books':books,
                                             'localip':localip,
                                             'thisyear':thisyear,
                                             'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':25,
                                                'hits' : paginator.count, 
                                             },context_instance=RequestContext(request))

###################################电影模块#############################################
def booktag(request,tname):
    global localip
    bts=DbBook.objects.filter(btype=tname)
    paginator = Paginator(bts,25)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    bts = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-5,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)   
    return render_to_response('dbtag.html',{
                                             'tag':tname,
                                             'bts':bts,
                                             'localip':localip,
                                             'thisyear':thisyear,
                                             'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':25,
                                                'hits' : paginator.count, 
                                             },context_instance=RequestContext(request))

    ###############################################################################
def movie(request):
    global localip
    mkeywords=request.GET.get('tag','top250')
    movies=DbMovie.objects.filter(Q(myear__contains=mkeywords))
    paginator = Paginator(movies,25)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    movies = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-5,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)   
    return render_to_response('movie.html',{
                                             'tag':mkeywords,
                                             'movies':movies,
                                             'localip':localip,
                                             'thisyear':thisyear,
                                             'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':25,
                                                'hits' : paginator.count, 
                                             },context_instance=RequestContext(request))

###################################相册模块部分代码#############################################
def showphoto(request):
    global localip
    types=PostType.objects.all
    photos=PhotoDB.objects.raw(u'SELECT auth_user.id,imagename,username,imageurl,imagesize,zanclick,uploadtime,MyBlog_photodb.id FROM MyBlog_photodb LEFT JOIN auth_user ON MyBlog_photodb.u=auth_user.id where MyBlog_photodb.is_public=0 ORDER BY MyBlog_photodb.uploadtime DESC')
    paginator = Paginator(list(photos),12)#使用paginator对象
    page = int(request.GET.get('p', '1'))#取当前页的号码
    photos = paginator.page(page).object_list #取paginator对象的当前页记录内容
    current = paginator.page(page)
    if page <= 5 and page<=paginator.num_pages-4:
        page_numbers=range(1,7)
    elif page <= 5 and page>paginator.num_pages-4:
        page_numbers=range(1,paginator.num_pages+1)
    elif (page > 5) and ( page >= paginator.num_pages - 4):
        page_numbers=range(paginator.num_pages-5,paginator.num_pages+1)
    elif (page > 5) and (  page <= paginator.num_pages - 4):
        page_numbers=range(page-4,page+4)   
    select={'day':connection.ops.date_trunc_sql('day','timestamp')}
    start_date='2010-1-1 0:0:0'
    end_date=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    cds=BlogPost.objects.filter(timestamp__range=(start_date, end_date)).extra(select={'year': "EXTRACT(year FROM timestamp)",
                                              'month': "EXTRACT(month from timestamp)"}
                                      ).values('year', 'month').annotate(number=Count('id')).order_by('-timestamp')[:20]
    
    return render_to_response('showphoto.html',{
                                                'types':types,    
                                                'cds':cds,
                                                'photos':photos,
                                                'localip':localip,
                                                'is_paginated': paginator.num_pages > 1,#是否分页
                                                'has_next': current.has_next(),
                                                'has_previous': current.has_previous(),
                                                'current_page': page,
                                                'next_page': page + 1,
                                                'previous_page': page - 1,
                                                'pages': paginator.num_pages,
                                                'page_numbers': page_numbers,
                                                'pagesize':12,
                                                'hits' : paginator.count, 
                                                 },context_instance=RequestContext(request))   
######################################################################################################
def zanphoto(request,pid):
    if pid<>'':
        zp=PhotoDB.objects.get(id=pid)
        zp.zanclick=zp.zanclick+1
        zp.save()
    return HttpResponse('<script type="text/JavaScript">alert("点赞成功！");window.location.href=document.referrer;</script>')  
###############################################################################################################
def updatephotobyid(request):
    if 'pcheckid' in request.GET and request.GET['pcheckid']:
        ids = request.GET.getlist('pcheckid',[])
        for id in ids:
            up=PhotoDB.objects.get(id=int(id))
            if up.is_public==0:
                up.is_public=1
                up.save()
            else:
                up.is_public=0
                up.save()            
    return HttpResponse('<script type="text/JavaScript">alert("设置成功！");window.location.href=document.referrer;</script>') 
######################################################################################
@csrf_protect
def downloadEntrez(request):
    if request.method == 'POST':
        global localip  
        GF_id=request.POST['filename']
        if GF_id <> '':
            #filename='E:\\gi_'+str(GF_id)+'.gb'
            from Bio import Entrez
            Entrez.email="kkds@slyyc.asia"
            handle=Entrez.efetch(db="nucleotide",id=str(GF_id),rettype="gb",retmode="text")
            #out_handle=open(filename,'w')
            from os import environ
            online = environ.get("APP_NAME", "")
            if online:
                import sae.const  
                access_key = sae.const.ACCESS_KEY  
                secret_key = sae.const.SECRET_KEY  
                appname = sae.const.APP_NAME  
                domain_name = "img1"  #刚申请的domain         
                import sae.storage
                s = sae.storage.Client()  
                ob = sae.storage.Object(handle.read())
                cname='gi_'+str(GF_id)+'.gb'

                fileurl = s.put(domain_name, cname, ob)  
                #out_handle.write(handle.read())
                handle.close()
                #out_handle.close()
                #record = SeqIO.read(fileurl,"genbank")
            #return HttpResponse('<script type="text/JavaScript">alert("下载成功！");window.location.href=document.referrer;</script>')
            return render_to_response('Entrez.html',{'fileurl':fileurl,'localip':localip,'thisyear':thisyear,},context_instance=RequestContext(request))
        else:
            return HttpResponse('<script type="text/JavaScript">alert("数据不合法&或者为空");window.location.href=document.referrer;</script>')
###########################################################################
def Entrez(request):
    global localip  
    return render_to_response('Entrez.html',{'localip':localip,'thisyear':thisyear,},context_instance=RequestContext(request))
##