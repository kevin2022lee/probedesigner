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
    if request.GET.get('genetype')=='Chinese_hamster':
        genes=GeneInfo8.objects.all().reverse()[:10] 
    if request.GET.get('genetype')=='Goat':
        genes=GeneInfo9.objects.all().reverse()[:10] 
    if request.GET.get('genetype')=='Guinea_pig':
        genes=GeneInfo10.objects.all().reverse()[:10] 
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
            table_num=request.POST["species"]
            if table_num=="":
                genes=GeneInfo.objects.filter(genename=genename)
            if  table_num=="1":
                genes=GeneInfo1.objects.filter(genename=genename)
            if  table_num=="2":
                genes=GeneInfo2.objects.filter(genename=genename)
            if  table_num=="3":
                genes=GeneInfo3.objects.filter(genename=genename)
            if  table_num=="4":
                genes=GeneInfo4.objects.filter(genename=genename)    
            if  table_num=="5":
                genes=GeneInfo5.objects.filter(genename=genename)
            if  table_num=="6":
                genes=GeneInfo6.objects.filter(genename=genename)
            if  table_num=="7":
                genes=GeneInfo7.objects.filter(genename=genename)
            if  table_num=="8":
                genes=GeneInfo8.objects.filter(genename=genename)
            if  table_num=="9":
                genes=GeneInfo9.objects.filter(genename=genename)
                
        return render_to_response('genedatabase/geneshow.html',{
                 'genes':genes,
                 'local':local,
                 'thisyear':thisyear
                 },context_instance=RequestContext(request))


def geneshow(request,specy,id):
    if specy=='Human':
        genes=GeneInfo.objects.filter(id__iexact=id)
    if specy=='Mouse':
        genes=GeneInfo1.objects.filter(id__iexact=id)
    if specy=='Rat':
        genes=GeneInfo2.objects.filter(id__iexact=id) 
    if specy=='At_Arabidopsis':
        genes=GeneInfo3.objects.filter(id__iexact=id)
    if specy=='C_elegans':
        genes=GeneInfo4.objects.filter(id__iexact=id)
    if specy=='Fruit_fly':
        genes=GeneInfo5.objects.filter(id__iexact=id)
    if specy=='Bovine':
        genes=GeneInfo6.objects.filter(id__iexact=id) 
    if specy=='Dog':
        genes=GeneInfo7.objects.filter(id__iexact=id)
    if specy=='Chinese_hamster':
        genes=GeneInfo8.objects.filter(id__iexact=id)
    if specy=='Goat':
        genes=GeneInfo9.objects.filter(id__iexact=id)
         
    return render_to_response('genedatabase/gene_details.html',{
        'local':local,
        'thisyear':thisyear,
        'genes':genes,
        },context_instance=RequestContext(request))
        
        
        
def loadmore(request,specy):
    if request.method=="POST":
        #异步刷新获取数据
        return HttpResponse("欢迎使用ajax")
        if specy=="Human":
            genes=GeneInfo.objects.all()
            pagesize = int(request.GET.get('ps', '10'))
            paginator = Paginator(genes,pagesize)#使用paginator对象
            page = int(request.GET.get('p', '1'))#取当前页的号码
            genes = paginator.page(page).object_list
            return HttpResponse("欢迎使用ajax")
    return render_to_response('genedatabase/load_more.html',{
        'local':local,
        'thisyear':thisyear,
        'stype':specy
        },context_instance=RequestContext(request))
        
        
        