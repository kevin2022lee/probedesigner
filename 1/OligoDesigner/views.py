#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
#from django.http import HttpResponse,HttpResponseRedirect

local='http:http://1.pdv1.applinzi.com'

def index(request):
    return render_to_response('bootstrap.html',{'local':local,},context_instance=RequestContext(request))
def probedesign(request):
    return render_to_response('probedesign.html',{'local':local,},context_instance=RequestContext(request))
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
global reverse
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
    return render_to_response('showprobe.html',{'local':local,'oligoseq':oligoseq,'seqlen':seqlen,'acount':acount,'ccount':ccount,'gcount':gcount,'tcount':tcount,'GC':GC,'MW':MW,'Tm':Tm,'OD':OD,'reverse':reverse,},context_instance=RequestContext(request))             
def probeList(s):
    count=0
    x=25
    strs=str(s)
    ProbeList=strs.split('')[0:x] 
    while(count < len(s)/x):
        m=25
        if count==0:
            ProbeList=strs.split('')[0:x]
        else:
            ProbeList=strs.split('')[m:m+x] 
        probedict={}
        if 55 < oligoTm(ProbeList) < 60:
            probedict['probe'+count]=ProbeList
        elif  oligoTm(ProbeList) <  55:
            y=1
            ProbeList=strs.split('',25+y) 
            while(55 < oligoTm(ProbeList) < 60):
                y+=1
                probedict['probe'+count]=ProbeList
            break
        elif oligoTm(ProbeList) >  60:
            z=1
            ProbeList=strs.split('',25-z)
            while(55 < oligoTm(ProbeList) < 60):
                z+=1
                probedict['probe'+count]=ProbeList
            break
        m=x+y-z#左右位移值
        x=m#校正x的正确值
        m+=m#m的值做累加
        count+=1#计数加1
        break    
    return probedict
                