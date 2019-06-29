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
    if request.GET.get('genetype')=='Human':
        genes=GeneInfo.objects.all().reverse()[:10]  
    if request.GET.get('genetype')=='Mouse':
        genes=GeneInfo1.objects.all().reverse()[:10]
    if request.GET.get('genetype')=='Rat':
        genes=GeneInfo2.objects.all().reverse()[:10] 
    if request.GET.get('genetype')=='At_Arabidopsis':
        genes=GeneInfo3.objects.all().reverse()[:10]   
    if request.GET.get('genetype')=='C_elegans':
        genes=GeneInfo4.objects.all().reverse()[:10]  
    if request.GET.get('genetype')=='Fruit_fly':
        genes=GeneInfo5.objects.all().reverse()[:10]
    if request.GET.get('genetype')=='Bovine':
        genes=GeneInfo6.objects.all().reverse()[:10] 
    if request.GET.get('genetype')=='Dog':
        genes=GeneInfo7.objects.all().reverse()[:10] 
    stype=request.GET.get("genetype",'Human')
    return render_to_response('genedatabase/genesearch.html',{
        'local':local,
        'thisyear':thisyear,
        'genes':genes,
        'stype':stype
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


def geneshow(request,specy,genename):
    if specy=='Human':
        genes=GeneInfo.objects.filter(genename=genename)
    if specy=='Mouse':
        genes=GeneInfo1.objects.filter(genename=genename)
    if specy=='Rat':
        genes=GeneInfo2.objects.filter(genename=genename) 
    if specy=='At_Arabidopsis':
        genes=GeneInfo3.objects.filter(genename=genename)
    if specy=='C_elegans':
        genes=GeneInfo4.objects.filter(genename=genename)
    if specy=='Fruit_fly':
        genes=GeneInfo5.objects.filter(genename=genename)
    if specy=='Bovine':
        genes=GeneInfo6.objects.filter(genename=genename) 
    if specy=='Dog':
        genes=GeneInfo7.objects.filter(genename=genename)
         
    return render_to_response('genedatabase/gene_details.html',{
        'local':local,
        'thisyear':thisyear,
        'genes':genes,
        },context_instance=RequestContext(request))
        