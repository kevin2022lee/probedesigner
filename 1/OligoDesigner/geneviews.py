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
    hots="""
        <div class="panel panel-success">
         <div class="panel-heading">
         热门检索基因
         </div>
        <div class="panel-body">
        <a href="http://www.probedesigner.cn/genedatabase/Human/52401/"><span class="label label-info label-small">GAPDH</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/51470/"><span class="label label-info label-small">TERT</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/1886/"><span class="label label-info label-small">Aff3</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/19382/"><span class="label label-info label-small">LOC103690090</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/AtArabidopsis/19999/"><span class="label label-info label-small">AT4G33770</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Celegans/200/"><span class="label label-info label-small">srz-32</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/52401/"><span class="label label-info label-small">GAPDH</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/51470/"><span class="label label-info label-small">TERT</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/1886/"><span class="label label-info label-small">Aff3</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/19382/"><span class="label label-info label-small">LOC103690090</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/AtArabidopsis/19999/"><span class="label label-info label-small">AT4G33770</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Celegans/200/"><span class="label label-info label-small">srz-32</span></a>

        </div>
        </div>
    """
    genes={} 
    if request.GET.get('genetype')=='Human':
        hots=''
        genes=GeneInfo.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Mouse':
        hots=''
        genes=GeneInfo1.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Rat':
        hots=''
        genes=GeneInfo2.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='AtArabidopsis':
        hots=''
        genes=GeneInfo3.objects.all().reverse()[:100]   
    if request.GET.get('genetype')=='Celegans':
        hots=''
        genes=GeneInfo4.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Fruitfly':
        hots=''
        genes=GeneInfo5.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Bovine':
        hots=''
        genes=GeneInfo6.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Dog':
        hots=''
        genes=GeneInfo7.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Chinesehamster':
        hots=''
        genes=GeneInfo8.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Goat':
        hots=''
        genes=GeneInfo9.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Guineapig':
        hots=''
        genes=GeneInfo10.objects.all().reverse()[:100] 
    #####################################################
    if request.GET.get('genetype')=='Zebrafish':
        hots=''
        genes=GeneInfo11.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Horse':
        hots=''
        genes=GeneInfo12.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Chicken':
        hots=''
        genes=GeneInfo13.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Soybean':
        hots=''
        genes=GeneInfo14.objects.all().reverse()[:100]   
    if request.GET.get('genetype')=='Nakedmolerat':
        hots=''
        genes=GeneInfo15.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='CynomolgusMonkey':
        hots=''
        genes=GeneInfo16.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Sheep':
        hots=''
        genes=GeneInfo17.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rabbit':
        hots=''
        genes=GeneInfo18.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rice':
        hots=''
        genes=GeneInfo19.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rhesusmonkeyhamster':
        hots=''
        genes=GeneInfo20.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Bakersyeast':
        hots=''
        genes=GeneInfo21.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Fissionyeast':
        hots=''
        genes=GeneInfo22.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Pig':
        hots=''
        genes=GeneInfo23.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Breadwheat':
        hots=''
        genes=GeneInfo24.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Winegrape':
        hots=''
        genes=GeneInfo25.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Westernclawedfrog':
        genes=GeneInfo26.objects.all().reverse()[:100] 
        hots=''
    if request.GET.get('genetype')=='Maize':
        hots=''
        genes=GeneInfo27.objects.all().reverse()[:100]        
    stype=request.GET.get("genetype",'')
    return render_to_response('genedatabase/genesearch.html',{
                                    'local':local,
                                    'thisyear':thisyear,
                                    'genes':genes,
                                    'hots':hots,
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
                ##########################
            if  table_num=="10":
                genes=GeneInfo10.objects.filter(genename=genename)
            if  table_num=="11":
                genes=GeneInfo11.objects.filter(genename=genename)
            if  table_num=="12":
                genes=GeneInfo12.objects.filter(genename=genename)
            if  table_num=="13":
                genes=GeneInfo13.objects.filter(genename=genename)    
            if  table_num=="14":
                genes=GeneInfo14.objects.filter(genename=genename)
            if  table_num=="15":
                genes=GeneInfo15.objects.filter(genename=genename)
            if  table_num=="16":
                genes=GeneInfo16.objects.filter(genename=genename)
            if  table_num=="17":
                genes=GeneInfo17.objects.filter(genename=genename)
            if  table_num=="18":
                genes=GeneInfo18.objects.filter(genename=genename)
                #######################################
            if  table_num=="19":
                genes=GeneInfo19.objects.filter(genename=genename)
            if  table_num=="20":
                genes=GeneInfo20.objects.filter(genename=genename)
            if  table_num=="21":
                genes=GeneInfo21.objects.filter(genename=genename)
            if  table_num=="22":
                genes=GeneInfo22.objects.filter(genename=genename)    
            if  table_num=="23":
                genes=GeneInfo23.objects.filter(genename=genename)
            if  table_num=="24":
                genes=GeneInfo24.objects.filter(genename=genename)
            if  table_num=="25":
                genes=GeneInfo25.objects.filter(genename=genename)
            if  table_num=="26":
                genes=GeneInfo26.objects.filter(genename=genename)
            if  table_num=="27":
                genes=GeneInfo27.objects.filter(genename=genename)
                
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
    if specy=='AtArabidopsis':
        genes=GeneInfo3.objects.filter(id__iexact=id)
    if specy=='Celegans':
        genes=GeneInfo4.objects.filter(id__iexact=id)
    if specy=='Fruitfly':
        genes=GeneInfo5.objects.filter(id__iexact=id)
    if specy=='Bovine':
        genes=GeneInfo6.objects.filter(id__iexact=id) 
    if specy=='Dog':
        genes=GeneInfo7.objects.filter(id__iexact=id)
    if specy=='Chinesehamster':
        genes=GeneInfo8.objects.filter(id__iexact=id)
    if specy=='Goat':
        genes=GeneInfo9.objects.filter(id__iexact=id)
    ####################################################
    if specy=='Guineapig':
        genes=GeneInfo10.objects.filter(id__iexact=id)
    if specy=='Zebrafish':
        genes=GeneInfo11.objects.filter(id__iexact=id)
    if specy=='Horse':
        genes=GeneInfo12.objects.filter(id__iexact=id) 
    if specy=='Chicken':
        genes=GeneInfo13.objects.filter(id__iexact=id)
    if specy=='Soybean':
        genes=GeneInfo14.objects.filter(id__iexact=id)
    if specy=='Nakedmolerat':
        genes=GeneInfo15.objects.filter(id__iexact=id)
    if specy=='CynomolgusMonkey':
        genes=GeneInfo16.objects.filter(id__iexact=id) 
    if specy=='Sheep':
        genes=GeneInfo17.objects.filter(id__iexact=id)
    if specy=='Rabbit':
        genes=GeneInfo18.objects.filter(id__iexact=id)
    if specy=='Rice':
        genes=GeneInfo19.objects.filter(id__iexact=id)
        #################################################
    if specy=='Rhesusmonkeyhamster':
        genes=GeneInfo20.objects.filter(id__iexact=id)
    if specy=='Bakersyeast':
        genes=GeneInfo21.objects.filter(id__iexact=id)
    if specy=='Fissionyeast':
        genes=GeneInfo22.objects.filter(id__iexact=id) 
    if specy=='Pig':
        genes=GeneInfo23.objects.filter(id__iexact=id)
    if specy=='Breadwheat':
        genes=GeneInfo24.objects.filter(id__iexact=id)
    if specy=='Winegrape':
        genes=GeneInfo25.objects.filter(id__iexact=id)
    if specy=='Westernclawedfrog':
        genes=GeneInfo26.objects.filter(id__iexact=id) 
    if specy=='Maize':
        genes=GeneInfo27.objects.filter(id__iexact=id)



         
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
        
def sightRNAsearch(request):
    hots="""
        <div class="panel panel-success">
         <div class="panel-heading">
         热门检索基因
         </div>
        <div class="panel-body">
        <a href="http://www.probedesigner.cn/genedatabase/Human/52401/"><span class="label label-info label-small">GAPDH</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/51470/"><span class="label label-info label-small">TERT</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/1886/"><span class="label label-info label-small">Aff3</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/19382/"><span class="label label-info label-small">LOC103690090</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/AtArabidopsis/19999/"><span class="label label-info label-small">AT4G33770</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Celegans/200/"><span class="label label-info label-small">srz-32</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/52401/"><span class="label label-info label-small">GAPDH</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Human/51470/"><span class="label label-info label-small">TERT</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/1886/"><span class="label label-info label-small">Aff3</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Mouse/19382/"><span class="label label-info label-small">LOC103690090</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/AtArabidopsis/19999/"><span class="label label-info label-small">AT4G33770</span></a>
        <a href="http://www.probedesigner.cn/genedatabase/Celegans/200/"><span class="label label-info label-small">srz-32</span></a>

        </div>
        </div>
    """
    genes={} 
    if request.GET.get('genetype')=='Human':
        hots=''
        genes=SightRNA.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Mouse':
        hots=''
        genes=SightRNA1.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Rat':
        hots=''
        genes=SightRNA2.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='AtArabidopsis':
        hots=''
        genes=SightRNA3.objects.all().reverse()[:100]   
    if request.GET.get('genetype')=='Celegans':
        hots=''
        genes=SightRNA5.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Fruitfly':
        hots=''
        genes=SightRNA11.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Bovine':
        hots=''
        genes=SightRNA4.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Dog':
        hots=''
        genes=SightRNA6.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Chinesehamster':
        hots=''
        genes=SightRNA9.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Goat':
        hots=''
        genes=SightRNA7.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Guineapig':
        hots=''
        genes=SightRNA8.objects.all().reverse()[:100] 
    #####################################################
    if request.GET.get('genetype')=='Zebrafish':
        hots=''
        genes=SightRNA10.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Horse':
        hots=''
        genes=GeneInfo12.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Chicken':
        hots=''
        genes=GeneInfo13.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Soybean':
        hots=''
        genes=GeneInfo14.objects.all().reverse()[:100]   
    if request.GET.get('genetype')=='Nakedmolerat':
        hots=''
        genes=GeneInfo15.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='CynomolgusMonkey':
        hots=''
        genes=GeneInfo16.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Sheep':
        hots=''
        genes=GeneInfo17.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rabbit':
        hots=''
        genes=GeneInfo18.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rice':
        hots=''
        genes=GeneInfo19.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Rhesusmonkeyhamster':
        hots=''
        genes=GeneInfo20.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Bakersyeast':
        hots=''
        genes=GeneInfo21.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Fissionyeast':
        hots=''
        genes=GeneInfo22.objects.all().reverse()[:100]  
    if request.GET.get('genetype')=='Pig':
        hots=''
        genes=GeneInfo23.objects.all().reverse()[:100]
    if request.GET.get('genetype')=='Breadwheat':
        hots=''
        genes=GeneInfo24.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Winegrape':
        hots=''
        genes=GeneInfo25.objects.all().reverse()[:100] 
    if request.GET.get('genetype')=='Westernclawedfrog':
        genes=GeneInfo26.objects.all().reverse()[:100] 
        hots=''
    if request.GET.get('genetype')=='Maize':
        hots=''
        genes=GeneInfo27.objects.all().reverse()[:100]        
    stype=request.GET.get("genetype",'')
    return render_to_response('sightrnadatabase/genesearch.html',{
                                    'local':local,
                                    'thisyear':thisyear,
                                    'genes':genes,
                                    'hots':hots,
                                    'stype':stype
        },context_instance=RequestContext(request))
    
def sgeneshow(request,specy,id):
    if specy=='Human':
        genes=SightRNA.objects.filter(id__iexact=id)
    if specy=='Mouse':
        genes=SightRNA1.objects.filter(id__iexact=id)
    if specy=='Rat':
        genes=SightRNA2.objects.filter(id__iexact=id) 
    if specy=='AtArabidopsis':
        genes=SightRNA3.objects.filter(id__iexact=id)
    if specy=='Celegans':
        genes=SightRNA5.objects.filter(id__iexact=id)
    if specy=='Fruitfly':
        genes=SightRNA11.objects.filter(id__iexact=id)
    if specy=='Bovine':
        genes=SightRNA4.objects.filter(id__iexact=id) 
    if specy=='Dog':
        genes=SightRNA6.objects.filter(id__iexact=id)
    if specy=='Chinesehamster':
        genes=SightRNA9.objects.filter(id__iexact=id)
    if specy=='Goat':
        genes=SightRNA7.objects.filter(id__iexact=id)
    ####################################################
    if specy=='Guineapig':
        genes=SightRNA8.objects.filter(id__iexact=id)
    if specy=='Zebrafish':
        genes=SightRNA10.objects.filter(id__iexact=id)
    if specy=='Horse':
        genes=GeneInfo12.objects.filter(id__iexact=id) 
    if specy=='Chicken':
        genes=GeneInfo13.objects.filter(id__iexact=id)
    if specy=='Soybean':
        genes=GeneInfo14.objects.filter(id__iexact=id)
    if specy=='Nakedmolerat':
        genes=GeneInfo15.objects.filter(id__iexact=id)
    if specy=='CynomolgusMonkey':
        genes=GeneInfo16.objects.filter(id__iexact=id) 
    if specy=='Sheep':
        genes=GeneInfo17.objects.filter(id__iexact=id)
    if specy=='Rabbit':
        genes=GeneInfo18.objects.filter(id__iexact=id)
    if specy=='Rice':
        genes=GeneInfo19.objects.filter(id__iexact=id)
        #################################################
    if specy=='Rhesusmonkeyhamster':
        genes=GeneInfo20.objects.filter(id__iexact=id)
    if specy=='Bakersyeast':
        genes=GeneInfo21.objects.filter(id__iexact=id)
    if specy=='Fissionyeast':
        genes=GeneInfo22.objects.filter(id__iexact=id) 
    if specy=='Pig':
        genes=GeneInfo23.objects.filter(id__iexact=id)
    if specy=='Breadwheat':
        genes=GeneInfo24.objects.filter(id__iexact=id)
    if specy=='Winegrape':
        genes=GeneInfo25.objects.filter(id__iexact=id)
    if specy=='Westernclawedfrog':
        genes=GeneInfo26.objects.filter(id__iexact=id) 
    if specy=='Maize':
        genes=GeneInfo27.objects.filter(id__iexact=id)



         
    return render_to_response('genedatabase/gene_details.html',{
        'local':local,
        'thisyear':thisyear,
        'genes':genes,
        },context_instance=RequestContext(request))
        