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
    global local
    return render_to_response('genedatabase/genesearch.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))

@csrf_protect
def gdbsearch(request):
    if request.method=="POST":
        genename=request.POST["search_text"] 
        if genename=="*" or genename=="":
            genes=GeneInfo.objects.filter(genename="GAPDH")
        else:
            genes=GeneInfo.objects.filter(genename=genename)
            if len(genes)== 0:
                genes={
                    'genename':'暂无相关信息',
                    'geneprobetype':'暂无相关信息',
                    'genedescription':'暂无相关信息',
                    'genesectiongroup':'暂无相关信息'
                    }
        return render_to_response('genedatabase/geneshow.html',{
                 'genes':genes,
                 'local':local,
                 'thisyear':thisyear
                 },context_instance=RequestContext(request))
    