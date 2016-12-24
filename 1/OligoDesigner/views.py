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
##############X-mer数值计算函数################
@csrf_protect                                                             
def x4merCalc(request):
    if request.method=="POST":
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
        
        uni_Aleader_seq=Seq("AAAACGGTAACTTCTTTATGCTTTGACTCAG", IUPAC.unambiguous_dna)
        uni_Aarms_seq=Seq("ATCTCAGTCTCGTTAATGGATTCCT", IUPAC.unambiguous_dna)
        uni_AP_seq=Seq("GATGTGGTTGTCGTACTT", IUPAC.unambiguous_dna)
        uni_PSCP_seq=Seq("CTCTTGGAAAGAAAGT", IUPAC.unambiguous_dna)
###########Server as CE Probe Weighting Factor##########################
        WF_CEtoLeaders=3
        WF_CEtoAMParms=20
        WF_CEtoAP=20
        WF_LEtoPSCP=0
###########Server as LE Probe Weighting Factor##########################
        WF_LEtoLeaders=0
        WF_LEtoAMParms=0
        WF_LEtoAP=0
        WF_CEtoPSCP=12
        
        calc_seq=Seq(request.POST['pseq'], IUPAC.unambiguous_dna).upper()
        arith = arithmetic()
        x4merlcs_Aleader=arith.lcs(str(uni_Aleader_seq),str(calc_seq))
        x4merlcslen_Aleader=arith.levenshtein(str(uni_Aleader_seq),str(calc_seq))
        x4merlcs_Aarms=arith.lcs(str(uni_Aarms_seq),str(calc_seq))
        x4merlcs_AP=arith.lcs(str(uni_AP_seq),str(calc_seq))
        x4merlcs_PSCP=arith.lcs(str(uni_PSCP_seq),str(calc_seq))
########与Aleader计算X-mer值############
        if len(x4merlcs_Aleader) >=4:
            x4mer_Aleaders=x4merlcs_Aleader+"-"+Seq(x4merlcs_Aleader,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_Aleader=[]
            score_x4mer_Aleader=[]
            data_Aleader={}
            while(i<len(x4merlcs_Aleader)-3):
                x4mer_Aleader.append(x4merlcs_Aleader[i:i+4]+"-"+Seq(x4merlcs_Aleader[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_Aleader.append(x4merScore(x4merlcs_Aleader[i:i+4]))
                i=i+1
            data_Aleader['x4mer_Aleader']=x4mer_Aleader
            data_Aleader['score_x4mer_Aleader']=score_x4mer_Aleader
            NSH_Score_Aleader_SACE=sum(data_Aleader['score_x4mer_Aleader'])*WF_CEtoLeaders
            NSH_Score_Aleader_SALE=sum(data_Aleader['score_x4mer_Aleader'])*WF_LEtoLeaders
        else:
            x4mer_Aleaders=""
            data_Aleader={'x4mer_Aleader':'-','score_x4mer_Aleader':'-'}
            NSH_Score_Aleader_SACE=0
            NSH_Score_Aleader_SALE=0
########与Aarms计算X-mer值############
        if len(x4merlcs_Aarms) >=4:
            x4mer_Aarmss=x4merlcs_Aarms+"-"+Seq(x4merlcs_Aarms,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_Aarms=[]
            score_x4mer_Aarms=[]
            data_Aarms={}
            while(i<len(x4merlcs_Aarms)-3):
                x4mer_Aarms.append(x4merlcs_Aarms[i:i+4]+"-"+Seq(x4merlcs_Aarms[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_Aarms.append(x4merScore(x4merlcs_Aarms[i:i+4]))
                i=i+1
            data_Aarms['x4mer_Aarms']=x4mer_Aarms
            data_Aarms['score_x4mer_Aarms']=score_x4mer_Aarms
            NSH_Score_Aarms_SACE=sum(data_Aarms['score_x4mer_Aarms'])*WF_CEtoAMParms
            NSH_Score_Aarms_SALE=sum(data_Aarms['score_x4mer_Aarms'])*WF_LEtoAMParms
        else:
            x4mer_Aarmss=""
            data_Aarms={'x4mer_Aarms':'-','score_x4mer_Aarms':'-'}
            NSH_Score_Aarms_SACE=0
            NSH_Score_Aarms_SALE=0
#####################与AP探针计算x-mer的值########
        if len(x4merlcs_AP) >=4:
            x4mer_APs=x4merlcs_AP+"-"+Seq(x4merlcs_AP,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_AP=[]
            score_x4mer_AP=[]
            data_AP={}
            while(i<len(x4merlcs_AP)-3):
                x4mer_AP.append(x4merlcs_AP[i:i+4]+"-"+Seq(x4merlcs_AP[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_AP.append(x4merScore(x4merlcs_AP[i:i+4]))
                i=i+1
            data_AP['x4mer_AP']=x4mer_AP
            data_AP['score_x4mer_AP']=score_x4mer_AP
            NSH_Score_AP_SACE=sum(data_AP['score_x4mer_AP'])*WF_CEtoAP
            NSH_Score_AP_SALE=sum(data_AP['score_x4mer_AP'])*WF_LEtoAP
        else:
            x4mer_APs=""
            data_AP={'x4mer_AP':'-','score_x4mer_AP':'-'}
            NSH_Score_AP_SACE=0
            NSH_Score_AP_SALE=0
##############与PSCP探针计算x-mer的值###############################
        if len(x4merlcs_PSCP) >=4:
            x4mer_PSCPs=x4merlcs_PSCP+"-"+Seq(x4merlcs_PSCP,IUPAC.unambiguous_dna).reverse_complement().tostring()
            i=0
            x4mer_PSCP=[]
            score_x4mer_PSCP=[]
            data_PSCP={}
            while(i<len(x4merlcs_PSCP)-3):
                x4mer_PSCP.append(x4merlcs_PSCP[i:i+4]+"-"+Seq(x4merlcs_PSCP[i:i+4],IUPAC.unambiguous_dna).reverse_complement().tostring())
                score_x4mer_PSCP.append(x4merScore(x4merlcs_PSCP[i:i+4]))
                i=i+1
            data_PSCP['x4mer_PSCP']=x4mer_PSCP
            data_PSCP['score_x4mer_PSCP']=score_x4mer_PSCP
            NSH_Score_PSCP_SACE=sum(data_PSCP['score_x4mer_PSCP'])*WF_LEtoPSCP
            NSH_Score_PSCP_SALE=sum(data_PSCP['score_x4mer_PSCP'])*WF_CEtoPSCP
        else:
            x4mer_PSCPs=""
            data_PSCP={'x4mer_PSCP':'-','score_x4mer_PSCP':'-'}
            NSH_Score_PSCP_SACE=0
            NSH_Score_PSCP_SALE=0
#######END############
        Total_NSH_SACE= NSH_Score_Aleader_SACE+NSH_Score_Aarms_SACE+NSH_Score_AP_SACE+NSH_Score_PSCP_SACE
        Total_NSH_SALE= NSH_Score_Aleader_SALE+NSH_Score_Aarms_SALE+NSH_Score_AP_SALE+NSH_Score_PSCP_SALE
        
#############模板渲染开始##########################
        return render_to_response('showcalcresult.html',{
                                                     'local':local,
                                                     'x4merlcs_Aleader':x4merlcs_Aleader,
                                                     'x4merlcslen_Aleader':x4merlcslen_Aleader,
                                                     'uni_Aleader_seq':uni_Aleader_seq,
                                                     'uni_Aarms_seq':uni_Aarms_seq,
                                                     'uni_AP_seq':uni_AP_seq,
                                                     'uni_PSCP_seq':uni_PSCP_seq,
                                                     'calc_seq':calc_seq,
                                                     'x4mer_Aleaders':x4mer_Aleaders,
                                                     'x4mer_Aarmss':x4mer_Aarmss,
                                                     'x4mer_APs':x4mer_APs,
                                                     'x4mer_PSCPs':x4mer_PSCPs,
                                                     'x4mer_Aleader':data_Aleader['x4mer_Aleader'],
                                                     'score_x4mer_Aleader':data_Aleader['score_x4mer_Aleader'],
                                                     'NSH_Score_Aleader_SACE':NSH_Score_Aleader_SACE,
                                                     'NSH_Score_Aleader_SALE':NSH_Score_Aleader_SALE,
                                                     'x4mer_Aarmss':x4mer_Aarmss,
                                                     'x4mer_Aarms':data_Aarms['x4mer_Aarms'],
                                                     'score_x4mer_Aarms':data_Aarms['score_x4mer_Aarms'],
                                                     'NSH_Score_Aarms_SACE':NSH_Score_Aarms_SACE,
                                                     'NSH_Score_Aarms_SACE':NSH_Score_Aarms_SACE,
                                                     'x4mer_APs':x4mer_APs,
                                                     'x4mer_AP':data_AP['x4mer_AP'],
                                                     'score_x4mer_AP':data_AP['score_x4mer_AP'],
                                                     'NSH_Score_AP_SACE':NSH_Score_AP_SACE,
                                                     'NSH_Score_AP_SALE':NSH_Score_AP_SALE,
                                                     'x4mer_PSCPs':x4mer_PSCPs,
                                                     'x4mer_PSCP':data_PSCP['x4mer_PSCP'],
                                                     'score_x4mer_PSCP':data_PSCP['score_x4mer_PSCP'],
                                                     'NSH_Score_PSCP_SACE':NSH_Score_PSCP_SACE,
                                                     'NSH_Score_PSCP_SACLE':NSH_Score_PSCP_SALE,
                                                     'Total_NSH_SACE':Total_NSH_SACE,
                                                     'Total_NSH_SALE':Total_NSH_SALE,
                                                     },context_instance=RequestContext(request))
def x4merScore(seq):
    SumAT=seq.count("A")+seq.count("T")
    SumGC=seq.count("G")+seq.count("C")
    Score=round((0.5*SumAT+1.0*SumGC)/4,3)
    return Score