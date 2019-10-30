#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
from django.core.context_processors import request
import pymysql


local='www.probedesigner.cn'
thisyear=time.strftime('%Y',time.localtime(time.time()))

def order(request):
    return render_to_response('order.html',{
                                    'local':local,
                                    'thisyear':thisyear,
        },context_instance=RequestContext(request))