#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
from django.core.context_processors import request
import pymysql


local='www.probedesigner.cn'
thisyear=time.strftime('%Y',time.localtime(time.time()))


def genesearch(request):
    genes={} 
    if request.GET.get('genetype'):
        genes=GeneInfo.objects.filter()[:10]  
    return render_to_response('genedatabase/genesearch.html',{
        'local':local,
        'thisyear':thisyear,
        'genes':genes
        },context_instance=RequestContext(request))

@csrf_protect
def gdbsearch(request):
    if request.method=="POST":
        genename=request.POST["search_text"] 
        if genename=="*" or genename=="":
            genes=GeneInfo.objects.filter(genename="GAPDH")
        else:
            genes=GeneInfo.objects.filter(genename=genename)

        return render_to_response('genedatabase/geneshow.html',{
                 'genes':genes,
                 'local':local,
                 'thisyear':thisyear
                 },context_instance=RequestContext(request))
    