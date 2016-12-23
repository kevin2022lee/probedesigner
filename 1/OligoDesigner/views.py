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

#######################实现最长公共字符查找##################################
class arithmetic():  
      
    def __init__(self):  
        pass  
    ''' 【编辑距离算法】 【levenshtein distance】 【字符串相似度算法】 '''
    
    def levenshtein(self,first,second):  
        if len(first) > len(second):  
            first,second = second,first  
        if len(first) == 0:  
            return len(second)  
        if len(second) == 0:  
            return len(first)  
        first_length = len(first) + 1  
        second_length = len(second) + 1  
        distance_matrix = [range(second_length) for x in range(first_length)]   
        #print distance_matrix  
        for i in range(1,first_length):  
            for j in range(1,second_length):  
                deletion = distance_matrix[i-1][j] + 1  
                insertion = distance_matrix[i][j-1] + 1  
                substitution = distance_matrix[i-1][j-1]  
                if first[i-1] != second[j-1]:  
                    substitution += 1  
                distance_matrix[i][j] = min(insertion,deletion,substitution)  
        #print distance_matrix  
        return distance_matrix[first_length-1][second_length-1]
    
    def lcs(self,first,second):  
        first_length = len(first)  
        second_length = len(second)  
        size = 0  
        x = 0  
        y = 0  
        matrix = [range(second_length) for x in range(first_length)]  
        #print matrix  
        for i in range(first_length):  
            for j in range(second_length):  
                #print i,j  
                if first[i] == second[j]:  
                    if i - 1 >= 0 and j - 1 >=0:  
                        matrix[i][j] = matrix[i-1][j-1] + 1  
                    else:  
                        matrix[i][j] = 1  
                    if matrix[i][j] > size:  
                        size = matrix[i][j]  
                        x = j  
                        y = i  
                else:  
                    matrix[i][j] = 0  
        #print matrix  
        #print size,x,y   
  
        return second[x-size+1:x+1]  
#######################################################################
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
        if filetype[0]==".gb" :
            record=SeqIO.parse(urlopen(fileurl),"genbank")
        elif filetype[0]==".fasta":
            record=SeqIO.parse(urlopen(fileurl),"fasta")
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
    return render_to_response('parselocalfile.html',{
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
def x4merCalc(request):
    if request.method=="POST":
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
        uni_seq=Seq("CCGCCAGCAAAGCTTTGGA", IUPAC.unambiguous_dna)
        calc_seq=Seq(request.POST['pseq'], IUPAC.unambiguous_dna).upper()
        arith = arithmetic()
        x4merlcs=arith.lcs(str(uni_seq),str(calc_seq))
        x4merlcslen=arith.levenshtein(str(uni_seq),str(calc_seq))
        if len(x4merlcs) >=4:
            x4mers=x4merlcs+"-"+Seq(x4merlcs,IUPAC.unambiguous_dna).reverse_complement().tostring()
            x4mer1=x4merlcs[0:4]+"-"+Seq(x4merlcs[0:4],IUPAC.unambiguous_dna).reverse_complement().tostring()
            x4mer2=x4merlcs[1:5]+"-"+Seq(x4merlcs[1:5],IUPAC.unambiguous_dna).reverse_complement().tostring()
            score_x4mer1=x4merScore(x4merlcs[0:4],len(x4merlcs))
            score_x4mer2=x4merScore(x4merlcs[1:5],len(x4merlcs))
        return render_to_response('showcalcresult.html',{
                                                     'local':local,
                                                     'x4merlcs':x4merlcs,
                                                     'x4merlcslen':x4merlcslen,
                                                     'uni_seq':uni_seq,
                                                     'calc_seq':calc_seq,
                                                     'x4mers':x4mers,
                                                     'x4mer1':x4mer1,
                                                     'x4mer2':x4mer2,
                                                     'score_x4mer1':score_x4mer1,
                                                     'score_x4mer2':score_x4mer2,
                                                     },context_instance=RequestContext(request))
def x4merScore(request,seq,len):
    SumAT=seq.count("A")+seq.count("T")
    SumGC=seq.count("G")+seq.count("C")
    Score=(0.5*SumAT+1.0*SumGC)/len
    return Score