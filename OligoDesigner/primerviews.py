#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
from django.db.models import Q
from django.core.context_processors import request
from primer3 import * 

local='www.probedesigner.cn'
thisyear=time.strftime('%Y',time.localtime(time.time()))

def primerdesigner(request):
    return render_to_response('primer3/primer.html',{
                                    'local':local,
                                    'thisyear':thisyear
        },context_instance=RequestContext(request))