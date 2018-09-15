#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
from views import *
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
def zzprobe(request):
    global local
    return render_to_response('zzprobe/zzprobe.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
def designbranch(request):
    global local
    return render_to_response('designbranch/designbranch.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
@csrf_protect  
def seqresolve(request):
    if request.method=='POST':
        content = request.FILES['file']
        name=content.name
        from os import environ  
        online = environ.get("APP_NAME", "")   
   
    if online:  
        import sae.const  
        access_key = sae.const.ACCESS_KEY  
        secret_key = sae.const.SECRET_KEY  
        appname = sae.const.APP_NAME  
        domain_name = "seq"  #刚申请的domain         
           
        import sae.storage
        s = sae.storage.Client()  
        ob = sae.storage.Object(content.read())
        cname=content.name
        cname_rb=base64.encodestring(datetime.now().strftime("%Y%m%d%H%M%S%f")+'_'+str(len(cname)))[:-3]+'.'+cname.split('.')[-1]
        fileurl = s.put(domain_name, cname_rb, ob)
        time.sleep(10)
        from Bio import Entrez,SeqIO
        import urllib
        from urllib import urlopen
        import re
        filetype=re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',fileurl)
#         header={
#             'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
#             }
        global record
        if filetype[0]==".gb" :
            record=SeqIO.parse(urlopen(fileurl),"genbank")
            #time.sleep(10)
        elif filetype[0]==".fasta":
            record=SeqIO.parse(urlopen(fileurl),"fasta")
            #time.sleep(10)
        nr=record.next()
################模板开始渲染######################################        
        if len(nr.annotations)!=0:
            source=nr.annotations['source']
            organism=nr.annotations['organism']
            taxonomy=nr.annotations['taxonomy']
            topology=nr.annotations['topology']
        else:
            source="N/A"
            organism="N/A"
            taxonomy="N/A"
            topology="N/A"
            
        cookie=Cookie.SimpleCookie()
        #cookie['sequence']=nr.seq
        #cookie['descri']=nr.description
        #request.session['description']=nr.description
        #request.session['sequence']=nr.seq
    response=render_to_response('zzprobe/parselocalfile.html',{
                                                       'local':local,
                                                       'thisyear':thisyear,
                                                       'filetype':filetype[0],
                                                       'local':local,
                                                       'accessid':nr.id,
                                                       'sequence':str(nr.seq),
                                                       'description':nr.description,
                                                       'name':nr.name,
                                                     #'dbxrefs':nr.dbxrefs[0],
                                                       'source':source,
                                                       'organism':organism,
                                                       'taxonomy':taxonomy,
                                                       'topology':topology,
                                                     },context_instance=RequestContext(request))
    response.set_cookie("seq",nr.seq)
    response.set_cookie("des",nr.description)
    return response
@csrf_protect  
def entrezremote(request):
    if request.method=="POST":
        from Bio import Entrez
        from Bio import SeqIO
        Entrez.email="kkds@slyyc.asia"
        SeqId=request.POST['seqid']
        Start=int(request.POST['start'])
        End=int(request.POST['end'])
        handle=Entrez.efetch(db="nucleotide",rettype="gb",retmote="text",id=SeqId)
        record=SeqIO.read(handle,"gb")
        time.sleep(10)
        handle.close()
        cookie=Cookie.SimpleCookie()
        response=render_to_response('zzprobe/parselocalfile.html',{
                                                       'local':local,
                                                       'thisyear':thisyear,
                                                       'filetype':'genbank',
                                                       'accessid':record.id,
                                                       'sequence':replace_RAGTC(str(record.seq[Start-1:End-1])),
                                                       'description':record.description,
                                                       'name':record.name,
                                                       #'dbxrefs':nr.dbxrefs[0],
                                                       'source':record.annotations['source'],
                                                       'organism':record.annotations['organism'],
                                                       'taxonomy':record.annotations['taxonomy'],
                                                       'topology':record.annotations['topology'],
                                                           },context_instance=RequestContext(request))
#         response.set_cookie("seq",replace_RAGTC(str(record.seq[Start-1:])))
        response.set_cookie("des",record.description)
        return response
#########远程访问Entrez数据库#####################    
@csrf_protect
def startzzprobedesign(request):
    if request.method=="POST":
        global local
        return render_to_response('zzprobe/startdesign.html',{
                                                      'local':local,
                                                      'thisyear':thisyear,
                                                      'sequence':request.POST['seq'],
                                                      'description':request.COOKIES.get('des',''),
                                                      },context_instance=RequestContext(request))

@csrf_protect    
def NNFzzprobe(req):
    if req.method=='POST':
        nonnshfilter=NonNSHFilter()
        probedict={}
        probelist=nonnshfilter.filterSequence(req.POST['seqtxt'])
        s=req.POST['seqtxt'].upper()
        probelist.append(len(s))
        for i in range(len(probelist)):
            if probelist[i]<len(s)-20:
#计算GC含量以及计算CE&LE 公式：
                probedict.setdefault('p'+str(probelist[i]),[reverseOligo(s[probelist[i]:probelist[i+1]]),probelist[i]])
        return render_to_response('zzprobe/showfilterprobe.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'probedict':probedict,
                                                     },context_instance=RequestContext(req))  
##################################################################
def PCXzzprobe(req):
    if req.method=='POST':
        dict_xmervalue=[]
        probe_xmer_list=[]
        probe_xmer_dict={}
        dict_value=req.POST.getlist('probedictvalue','')
        dict_key=req.POST.getlist('probedictkey','')
        dict_length=req.POST.getlist('probelength','')
        xmerclac=CalcNSH()
        for i in range(len(dict_value)):
            dict_xmervalue.append(xmerclac.xmerCalc(dict_value[i]))
        for v in range(len(dict_xmervalue)):
            probe_xmer_dict.setdefault(dict_key[v],[dict_xmervalue[v],int(dict_length[v]),dict_value[v],oligoGC(dict_value[v])])
        probe_xmer_list=sorted(probe_xmer_dict.items(),key=lambda x:x[1][1])
        return render_to_response('zzprobe/xmerscore.html',{
                                                                              'local':local,
                                                                              'thisyear':thisyear,
                                                                              'probe_xmer_list':probe_xmer_list,
                                                                              },context_instance=RequestContext(req))
#########################CE&LE cross#################################
###################################################
def zzProbeSetsXmer(req):
    if req.method=="POST":
        LE_plist=[]
        list_pkey=req.POST.getlist("pkey")
        list_pseq=req.POST.getlist("pseq")
        list_LE=req.POST.getlist("LEcheck")
        zzprobesets_list=[]
        for i in range(len(list_pkey)):
            zzprobesets_list.append((list_pkey[i],list_pseq[i],list_LE[i]))
        for j in range(len(zzprobesets_list)):
            if zzprobesets_list[j][2]=="LE":
                LE_plist.append((zzprobesets_list[j][0],zzprobesets_list[j][1]))
        return render_to_response('zzprobe/showceleNSH.html',{
                                                        'local':local,
                                                        'thisyear':thisyear,
                                                        'LE_plist':LE_plist,
                                                        },context_instance=RequestContext(req))   
##################################Generate probe sets#####################################################                                                        
def GeneratezzProbesets(req):
    if req.method=="POST":
        probesname=req.POST.getlist("probename")
        probesseq=req.POST.getlist("probeseq")
        probesfunc=req.POST.getlist("probefunc")
        probesets_list=[]
        for i in range(len(probesname)):
            probesets_list.append((probesname[i],probesseq[i],probesfunc[i]))
        LE_final_list=[]
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="LE":
                LE_final_list.append((probesets_list[j][0],probesets_list[j][1]))
        LE_final_final_list=[]
        for k in range(len(LE_final_list)):
            if LE_final_list.index(LE_final_list[k])%2==0:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTgaagttaccgtttt'))
            else:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTctgagtcaaagcat'))
        return render_to_response('zzprobe/generateprobes.html',{
                                      'local':local,
                                      'thisyear':thisyear,
                                      'LE_final_final_list':LE_final_final_list,
                                      },context_instance=RequestContext(req))