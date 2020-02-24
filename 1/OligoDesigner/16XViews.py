#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
import sys,urllib
import base64
import Cookie
from STXmerCalcNSH import *
from arithMetic import *
from searchProbe import *
from XmerCalcCELENSH import *
from django.core.context_processors import request

##############################################注释分界线#######################################################


local='www.probedesigner.cn'
#local='127.0.0.1:8000'
thisyear=time.strftime('%Y',time.localtime(time.time()))

#######################实现最长公共字符查找##################################

def stxpd(request):
    global local
    return render_to_response('16xpd/16xpd.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))