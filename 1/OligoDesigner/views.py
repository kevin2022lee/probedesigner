#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect,csrf_exempt
#from django.http import HttpResponse,HttpResponseRedirect
import time
from datetime import datetime
import sys,urllib
import base64
local='pdv1.applinzi.com'

def index(request):
    global local
    return render_to_response('bootstrap.html',{'local':local,},context_instance=RequestContext(request))
def probedesign(request):
    global local
    return render_to_response('probedesign.html',{'local':local,},context_instance=RequestContext(request))
def entrez(request):
    global local
    return render_to_response('entrez.html',{'local':local,},context_instance=RequestContext(request))
def fromfile(request):
    global local
    return render_to_response('fromfile.html',{'local':local,},context_instance=RequestContext(request))
def test(request):
    global local
    return render_to_response('test.html',{'local':local,},context_instance=RequestContext(request))
def oligoGC(s):
    if len(s)!= 0:
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')
    return round(100*(gcount+ccount)/(gcount+ccount+acount+tcount))
def oligoMW(s):
    if len(s)!=0:
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')
    return round(313.21 * acount + 329.21 * gcount + 289.18 * ccount + 304.19 * tcount  - 60.96)
def oligoTm(s):
    if len(s)!= 0:
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T') 
        if len(s)<14:
            TmValue=round(2*(acount+tcount)+4*(gcount+ccount))
        else:
            TmValue=round(64.9+41*((gcount+ccount-16.4)/len(s)))
    else:
        TmValue=0
    return TmValue
def oligoOD(s):
    if len(s)!= 0:
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')        
        ODValue=round((1000/(gcount*8.1+ccount*6.1+acount*13.3+tcount*7.9))*1000)/1000
    else:
        ODValue=0
    return ODValue
#################################碱基互补配对函数######################################################################   
re_seq=''
def reverseOligo(ss):
    if len(ss)!= 0:
        strss=str(ss)
        for s in strss:
            global re_seq
            if s=='A':
                re_s='T'
                re_seq=re_seq+re_s
            elif s=='T':
                re_s='A'
                re_seq=re_seq+re_s
            elif s=='G':
                re_s='C'
                re_seq=re_seq+re_s
            elif s=='C':
                re_s='G'
                re_seq=re_seq+re_s
    return re_seq[::-1]
##############################################################功能实现代码区############################################
@csrf_protect
def subseq(request):
    if request.method=='POST':
        oligoseq=request.POST['oligoBox']
        seqlen=len(oligoseq)
        if seqlen !=0:
            acount=oligoseq.count('A')
            ccount=oligoseq.count('C')
            gcount=oligoseq.count('G')
            tcount=oligoseq.count('T')
            GC=oligoGC(oligoseq)
            MW=oligoMW(oligoseq)
            Tm=oligoTm(oligoseq)
            OD=oligoOD(oligoseq)
            reverse=reverseOligo(oligoseq)
            pl=probeList(reverse)
        else:
            acount=0
            ccount=0
            gcount=0
            tcount=0
            GC=0
            MW=0
            Tm=0
            OD=0
            reverse=''
            pl=''
    return render_to_response('showprobe.html',{'local':local,'oligoseq':oligoseq,'seqlen':seqlen,'acount':acount,'ccount':ccount,'gcount':gcount,'tcount':tcount,'GC':GC,'MW':MW,'Tm':Tm,'OD':OD,'reverse':reverse,'pl':pl,},context_instance=RequestContext(request))             
def probeList(s):
    probedict={}
    count=1
    while(count<=len(s)/25):
        begin=25*count-25
        end=25*count
        probedict.setdefault('probe'+str(count),s[begin:end])
        count=count+1
        if count>=len(s)/25:
            probedict.setdefault('probe'+str(count+1),s[25*count:len(s)])
            break        
    return probedict
 ###############################################################################################################
def downloadentrez(request):
    if request.method=='POST':
        gid=request.POST['filename']
        from Bio import Entrez
        Entrez.email="kkds@slyyc.asia"
        handle=Entrez.efetch(db="nucleotide",id=str(gid),rettype="gb",retmode="xml")
        record=Entrez.read(handle, validate=False)
        request.session['sequence']=record[0]['GBSeq_sequence']
        aversion="N/A"
        udate="N/A" 
        protein_seq="N/A"
        return render_to_response('showentrez.html',{
                                                     'local':local,
                                                     'oligoseq':record[0]['GBSeq_sequence'],
                                                     'seqlen':record[0]['GBSeq_length'],
                                                     'cdate':record[0]['GBSeq_create-date'],
                                                     'taxonomy':record[0]['GBSeq_taxonomy'],
                                                     'organism':record[0]['GBSeq_organism'],
                                                     'locus':record[0]['GBSeq_locus'],
                                                     'source':record[0]['GBSeq_source'],
                                                     'topology':record[0]['GBSeq_topology'],
                                                     'division':record[0]['GBSeq_division'],
                                                     'accession_version': aversion,
                                                     'update_date':udate ,
                                                     'strandedness':record[0]['GBSeq_strandedness'],
                                                     'definition':record[0]['GBSeq_definition'],
                                                     'protein_seq':protein_seq,
                                                     },context_instance=RequestContext(request))
    else:
        return HttpResponse("<script>alert(‘非法参数的进入！’)</script>")
def entreztoxml(request):
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
        from Bio import Entrez,SeqIO
        import urllib
        from urllib import urlopen
        import re
        filetype=re.findall(r'\.[^.\\/:*?"<>|\r\n]+$',fileurl)
        global record
        if filetype==".gb" :
            record=SeqIO.parse(urlopen(fileurl),"genbank")
        elif filetype==".fasta":
            record=SeqIO.parse(urlopen(fileurl),"fasta")
        nr=record.next()
################模板开始渲染######################################        

    return render_to_response('parselocalfile.html',{
                                                             'filetype':filetype,
                                                             'local':local,
                                                             'accessid':nr.id,
                                                             'sequence':nr.seq,
                                                             'description':nr.decription,
                                                             'name':nr.name,
                                                             'dbxrefs':nr.dbxrefs[0],
                                                             'source':nr.annotations['source'],
                                                             'organism':nr.annotations['organism'],
                                                             'taxonomy':nr.annotations['taxonomy'],
                                                             'topology':nr.annotations['topology'],
                                                             },context_instance=RequestContext(request))
    