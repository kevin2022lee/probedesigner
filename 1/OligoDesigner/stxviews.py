#coding:utf-8
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import time
from datetime import datetime
from models import *
import sys,urllib
import base64
import Cookie
from STXmerCalcNSH import *
from arithMetic import *
from searchProbe import *
from XmerCalcCELENSH import *
from django.core.context_processors import request

##############################################注释分界线#######################################################


local='www.probedesigner.cn'
#local='127.0.0.1:8000'
thisyear=time.strftime('%Y',time.localtime(time.time()))

#######################实现最长公共字符查找##################################

def stxpd(request):
    global local
    return render_to_response('16xpd/16xpd.html',{'local':local,'thisyear':thisyear},context_instance=RequestContext(request))
@csrf_protect  
def fileparse(request):
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
    response=render_to_response('16xpd/16xpdparse_result.html',{
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
##############X-mer数值计算函数################
@csrf_protect  
def entrezparse(request):
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
        response=render_to_response('16xpd/16xpdparse_result.html',{
                                                       'local':local,
                                                       'thisyear':thisyear,
                                                       'filetype':'genbank',
                                                       'accessid':record.id,
                                                       'sequence':str(record.seq[Start-1:End]),
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
def stxpd_design(request):
    if request.method=="POST":
        global local
        return render_to_response('16xpd/16xdesign.html',{
                                                      'local':local,
                                                      'thisyear':thisyear,
                                                      'sequence':list(request.POST['seq']),
                                                      'description':request.COOKIES.get('des',''),
                                                      },context_instance=RequestContext(request))
def reverseOligo(ss):
    if len(ss)!= 0:
        re_seq=''
        strss=str(ss)
        for s in strss:
#             global re_seq
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
            elif s=='R':
                re_s='Y'
                re_seq=re_seq+re_s
            elif s=='Y':
                re_s='R'
                re_seq=re_seq+re_s
            elif s=='M':
                re_s='K'
                re_seq=re_seq+re_s
            elif s=='K':
                re_s='M'
                re_seq=re_seq+re_s
            elif s=='S':
                re_s='S'
                re_seq=re_seq+re_s
            elif s=='W':
                re_s='W'
                re_seq=re_seq+re_s
            elif s=='H':
                re_s='D'
                re_seq=re_seq+re_s
            elif s=='B':
                re_s='V'
                re_seq=re_seq+re_s
            elif s=='V':
                re_s='B'
                re_seq=re_seq+re_s
            elif s=='D':
                re_s='H'
                re_seq=re_seq+re_s
            elif s=='N':
                re_s='N'
                re_seq=re_seq+re_s
            
    return re_seq[::-1]
##############################################################功能实现代码区############################################
@csrf_protect    
def stxprobefilter(req):
    if req.method=='POST':
        nonnshfilter=NonNSHFilter()
        probedict={}
        probedict1={}
        probedict2={}
        seqtxt=''.join(req.POST.getlist('seqtxt'))
        probelist=nonnshfilter.filterSequence(seqtxt,52,58)
        probelist1=nonnshfilter.filterSequence(seqtxt,52,55)
        probelist2=nonnshfilter.filterSequence(seqtxt,48,52)
        s=seqtxt.upper()
        probelist.append(len(s))
        probelist1.append(len(s))
        probelist2.append(len(s))
        for i in range(len(probelist)):
            if probelist[i]<len(s)-20:
#计算GC含量以及计算CE&LE 公式：
                probedict.setdefault('p'+str(probelist[i]),[reverseOligo(s[probelist[i]:probelist[i+1]]),probelist[i]])
        for i in range(len(probelist1)):
            if probelist1[i]<len(s)-20:
                probedict1.setdefault('p'+str(probelist1[i]),[reverseOligo(s[probelist1[i]:probelist1[i+1]]),probelist1[i]])
        for i in range(len(probelist2)):
            if probelist2[i]<len(s)-20:
                probedict2.setdefault('p'+str(probelist2[i]),[reverseOligo(s[probelist2[i]:probelist2[i+1]]),probelist2[i]])
        return render_to_response('16xpd/showstxprobe.html',{
                                                     'local':local,
                                                     'thisyear':thisyear,
                                                     'seqtxt':seqtxt,
                                                     'probedict':probedict,
                                                     'probedict1':probedict1,
                                                     'probedict2':probedict2,
                                                     },context_instance=RequestContext(req))  
##################################################################
def oligoGC(s):
    if len(s)!= 0:
        s=s.upper()
        acount=s.count('A')
        ccount=s.count('C')
        gcount=s.count('G')
        tcount=s.count('T')
    return round(100*(gcount+ccount)/(gcount+ccount+acount+tcount))

def stxprobeXmers(req):
    if req.method=='POST':
        dict_xmervalue=[]
        probe_xmer_list=[]
        probe_xmer_dict={}
        dict_value=req.POST.getlist('probedictvalue','')
        dict_key=req.POST.getlist('probedictkey','')
        dict_length=req.POST.getlist('probelength','')
        stxmerclac=STXCalcNSH()
        for i in range(len(dict_value)):
            dict_xmervalue.append(stxmerclac.xmerCalc(dict_value[i]))
        for v in range(len(dict_xmervalue)):
            probe_xmer_dict.setdefault(dict_key[v],[dict_xmervalue[v],int(dict_length[v]),dict_value[v],oligoGC(dict_value[v])])
        probe_xmer_list=sorted(probe_xmer_dict.items(),key=lambda x:x[1][1])
        return render_to_response('16xpd/showxmerscore.html',{
                                                                              'local':local,
                                                                              'thisyear':thisyear,
                                                                              'probe_xmer_list':probe_xmer_list,
                                                                              },context_instance=RequestContext(req))
#########################CE&LE cross#################################

def xpdProbeSetsXmer(req):
    if req.method=="POST":
        CE_plist=[]
        LE_plist=[]
        BL_plist=[]
        list_pkey=req.POST.getlist("pkey")
        list_pseq=req.POST.getlist("pseq")
        list_CE=req.POST.getlist("CEcheck")
        list_LE=req.POST.getlist("LEcheck")
        list_BL=req.POST.getlist("BLcheck")
        probesets_list=[]
        for i in range(len(list_pkey)):
            probesets_list.append((list_pkey[i],list_pseq[i],list_CE[i],list_LE[i],list_BL[i]))
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CE":
                CE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][3]=="LE":
                LE_plist.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][4]=="BL":
                BL_plist.append((probesets_list[j][0],probesets_list[j][1]))
        xmerclaccele=CalcCELENSH()
        CEtoLE_score_list=[]
        CEtoLE_score=[]
        LE_plist1=[]
        LE_plist2=[]  
        LE_plist3=[]
        LE_plist4=[]
        LE_plist5=[]
        LE_plist6=[]
        LE_plist7=[]
        LE_plist8=[]
        LE_plist9=[]
        LE_plist10=[]
        LE_plist11=[]
        LE_plist12=[]
        LE_plist13=[]
        len_lep=len(LE_plist)
        if len_lep<=15:
            LE_plist1=LE_plist[0:len(LE_plist)]
        elif 16<len_lep<=30:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:len(LE_plist)]
        elif 31<len_lep<=45:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:len(LE_plist)]
        elif 46<len_lep<=60:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:len(LE_plist)]
        elif 61<len_lep<=75:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:len(LE_plist)]
        elif 76<len_lep<=90:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:len(LE_plist)]
        elif 91<len_lep<=105:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:len(LE_plist)]
        elif 106<len_lep<=120:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:len(LE_plist)]
        elif 121<len_lep<=135:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:120]
            LE_plist9=LE_plist[120:len(LE_plist)]
        elif 135<len_lep<=150:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:120]
            LE_plist9=LE_plist[120:135]
            LE_plist10=LE_plist[134:len(LE_plist)]
        elif 150<len_lep<=165:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:120]
            LE_plist9=LE_plist[120:135]
            LE_plist10=LE_plist[120:135]
            LE_plist11=LE_plist[135:len(LE_plist)]
        elif 165<len_lep<=180:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:120]
            LE_plist9=LE_plist[120:135]
            LE_plist10=LE_plist[120:135]
            LE_plist11=LE_plist[135:150]
            LE_plist12=LE_plist[150:len(LE_plist)]
        elif 180<len_lep<=195:
            LE_plist1=LE_plist[0:15]
            LE_plist2=LE_plist[15:30]  
            LE_plist3=LE_plist[30:45]
            LE_plist4=LE_plist[45:60]
            LE_plist5=LE_plist[60:75]
            LE_plist6=LE_plist[75:90]
            LE_plist7=LE_plist[90:105]
            LE_plist8=LE_plist[105:120]
            LE_plist9=LE_plist[120:135]
            LE_plist10=LE_plist[120:135]
            LE_plist11=LE_plist[135:150]
            LE_plist12=LE_plist[150:165]
            LE_plist13=LE_plist[165:len(LE_plist)]    
        for c in range(len(CE_plist)):
            for l in range(len(LE_plist)):
                CEtoLE_score.append(xmerclaccele.xmerCalcCELE(CE_plist[c][1], LE_plist[l][1]))
            CEtoLE_score_list.append((CE_plist[c][0],CEtoLE_score[len_lep*c:(c+1)*len_lep]))
            
        CEtoLE_score_list1=[]
        CEtoLE_score_list2=[]
        CEtoLE_score_list3=[]
        CEtoLE_score_list4=[]
        CEtoLE_score_list5=[]
        CEtoLE_score_list6=[]
        CEtoLE_score_list7=[]
        CEtoLE_score_list8=[]
        CEtoLE_score_list9=[]
        CEtoLE_score_list10=[]
        CEtoLE_score_list11=[]
        CEtoLE_score_list12=[]
        CEtoLE_score_list13=[]
        
        if len_lep<=15:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:len_lep]))
        elif 15<len_lep<=30:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:len_lep]))
        elif 30<len_lep<=45:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:len_lep]))
        elif 45<len_lep<=60:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:len_lep]))
        elif 60<len_lep<=75:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:len_lep]))
        elif 75<len_lep<=90:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:len_lep]))
        elif 90<len_lep<=105:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:len_lep]))    
        elif 105<len_lep<=120:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:len_lep]))  
                
        elif 120<len_lep<=135:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:120]))
                CEtoLE_score_list9.append((clsl[0],clsl[1][120:len_lep]))  
                
        elif 135<len_lep<=150:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:120])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][120:135]))
                CEtoLE_score_list9.append((clsl[0],clsl[1][135:150]))
                CEtoLE_score_list10.append((clsl[0],clsl[1][150:len_lep])) 
        
        elif 150<len_lep<=165:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:120])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][120:135]))
                CEtoLE_score_list9.append((clsl[0],clsl[1][135:150]))
                CEtoLE_score_list10.append((clsl[0],clsl[1][150:165]))
                CEtoLE_score_list11.append((clsl[0],clsl[1][165:len_lep]))
        
        
        elif 165<len_lep<=180:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:120])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][120:135]))
                CEtoLE_score_list9.append((clsl[0],clsl[1][135:150]))
                CEtoLE_score_list10.append((clsl[0],clsl[1][150:165]))
                CEtoLE_score_list11.append((clsl[0],clsl[1][165:180]))
                CEtoLE_score_list12.append((clsl[0],clsl[1][180:len_lep]))
        
        elif 180<len_lep<=195:
            for clsl in CEtoLE_score_list:
                CEtoLE_score_list1.append((clsl[0],clsl[1][0:15]))
                CEtoLE_score_list2.append((clsl[0],clsl[1][15:30]))
                CEtoLE_score_list3.append((clsl[0],clsl[1][30:45]))
                CEtoLE_score_list4.append((clsl[0],clsl[1][45:60]))
                CEtoLE_score_list5.append((clsl[0],clsl[1][60:75])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][75:90]))
                CEtoLE_score_list7.append((clsl[0],clsl[1][90:105]))
                CEtoLE_score_list8.append((clsl[0],clsl[1][105:120])) 
                CEtoLE_score_list6.append((clsl[0],clsl[1][120:135]))
                CEtoLE_score_list9.append((clsl[0],clsl[1][135:150]))
                CEtoLE_score_list10.append((clsl[0],clsl[1][150:165]))
                CEtoLE_score_list11.append((clsl[0],clsl[1][165:180]))
                CEtoLE_score_list12.append((clsl[0],clsl[1][180:195]))
                CEtoLE_score_list12.append((clsl[0],clsl[1][195:len_lep]))
                
        return render_to_response('16xpd/showceleNSH.html',{
                                                        'local':local,
                                                        'thisyear':thisyear,
                                                        'len_lep':len_lep,
                                                        'LE_plist':LE_plist,
                                                        'LE_plist1':LE_plist1,
                                                        'LE_plist2':LE_plist2,
                                                        'LE_plist3':LE_plist3,
                                                        'LE_plist4':LE_plist4,
                                                        'LE_plist5':LE_plist5,
                                                        'LE_plist6':LE_plist6,
                                                        'LE_plist7':LE_plist7,
                                                        'LE_plist8':LE_plist8,
                                                        'LE_plist9':LE_plist9,
                                                        'LE_plist10':LE_plist10,
                                                        'LE_plist11':LE_plist11,
                                                        'LE_plist12':LE_plist12,
                                                        'LE_plist13':LE_plist13,
                                                        'CE_plist':CE_plist,
                                                        'BL_plist':BL_plist,
                                                        'CEtoLE_score_list':CEtoLE_score_list,
                                                        'CEtoLE_score_list1':CEtoLE_score_list1,
                                                        'CEtoLE_score_list2':CEtoLE_score_list2,
                                                        'CEtoLE_score_list3':CEtoLE_score_list3,
                                                        'CEtoLE_score_list4':CEtoLE_score_list4,
                                                        'CEtoLE_score_list5':CEtoLE_score_list5,
                                                        'CEtoLE_score_list6':CEtoLE_score_list6,
                                                        'CEtoLE_score_list7':CEtoLE_score_list7,
                                                        'CEtoLE_score_list8':CEtoLE_score_list8,
                                                        'CEtoLE_score_list9':CEtoLE_score_list9,
                                                        'CEtoLE_score_list10':CEtoLE_score_list10,
                                                        'CEtoLE_score_list11':CEtoLE_score_list11,
                                                        'CEtoLE_score_list12':CEtoLE_score_list12,
                                                        'CEtoLE_score_list13':CEtoLE_score_list13,
                                                        },context_instance=RequestContext(req))   
##################################Generate probe sets#####################################################
def xpdGenerateProbeset(req):
    if req.method=="POST" and req.POST.get("ampbtn")=="1":
        probesname=req.POST.getlist("probename")
        probesseq=req.POST.getlist("probeseq")
        probesfunc=req.POST.getlist("probefunc")
        probesets_list=[]
        for i in range(len(probesname)):
            probesets_list.append((probesname[i],probesseq[i],probesfunc[i]))
        CE_final_list=[]
        LE_final_list=[]
        BL_final_list=[]
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CP":
                CE_final_list.append((probesets_list[j][0],probesets_list[j][1]+'tttttCTCTTGGAAAGAAAGT'))
            if probesets_list[j][2]=="BL":
                BL_final_list.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][2]=="BP":
                LE_final_list.append((probesets_list[j][0],probesets_list[j][1]))
        LE_final_final_list=[]
        for k in range(len(LE_final_list)):
            if LE_final_list.index(LE_final_list[k])%2==0:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTgaagttaccgtttt'))
            else:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'TTTTTctgagtcaaagcat'))
        return render_to_response('generateprobes.html',{
                                      'local':local,
                                      'thisyear':thisyear,
                                      'CE_final_list':CE_final_list,
                                      'BL_final_list':BL_final_list,
                                      'LE_final_final_list':LE_final_final_list,
                                      },context_instance=RequestContext(req))
    else:
        probesname=req.POST.getlist("probename")
        probesseq=req.POST.getlist("probeseq")
        probesfunc=req.POST.getlist("probefunc")
        probesets_list=[]
        for i in range(len(probesname)):
            probesets_list.append((probesname[i],probesseq[i],probesfunc[i]))
        CE_final_list=[]
        LE_final_list=[]
        BL_final_list=[]
        for j in range(len(probesets_list)):
            if probesets_list[j][2]=="CP":
                CE_final_list.append((probesets_list[j][0],probesets_list[j][1]+'TTTTTctcttggaaagaaagt'))
            if probesets_list[j][2]=="BL":
                BL_final_list.append((probesets_list[j][0],probesets_list[j][1]))
            if probesets_list[j][2]=="BP":
                LE_final_list.append((probesets_list[j][0],probesets_list[j][1]))
        LE_final_final_list=[]
        for k in range(len(LE_final_list)):
            if LE_final_list.index(LE_final_list[k])%2!=0:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'tttttCTCGGTAAATACAG'))
            else:
                LE_final_final_list.append((LE_final_list[k][0],LE_final_list[k][1]+'tttttGTAATAGCTTGTCT'))
        return render_to_response('generateprobes.html',{
                                      'local':local,
                                      'thisyear':thisyear,
                                      'CE_final_list':CE_final_list,
                                      'BL_final_list':BL_final_list,
                                      'LE_final_final_list':LE_final_final_list,
                                      },context_instance=RequestContext(req))
        
############################################################################################################