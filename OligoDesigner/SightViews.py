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
from xmerCalcNSH import *
from arithMetic import *
from searchProbe import *
from XmerCalcCELENSH import *
from django.core.context_processors import request

local='www.probedesigner.cn'
#local='127.0.0.1:8000'
thisyear=time.strftime('%Y',time.localtime(time.time()))

def sightintro(request):
    global local
    return render_to_response('sightintro.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))