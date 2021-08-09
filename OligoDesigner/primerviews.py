#coding:utf-8
import time
#import primer3 
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response

local='www.probedesigner.cn'
thisyear=time.strftime('%Y',time.localtime(time.time()))

def primerdesigner(request):
    return render_to_response('primer3/primer.html',{
                                    'local':local,
                                    'thisyear':thisyear
        },context_instance=RequestContext(request))