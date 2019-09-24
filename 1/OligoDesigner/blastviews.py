from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt
import numpy as np
import time
from datetime import datetime
from django.core.context_processors import request

local='www.probedesigner.cn'
thisyear=time.strftime('%Y',time.localtime(time.time()))

def MSA(request):
    return render_to_response('msa/msa.html',
                              {'local':local,
                               'thisyear':thisyear,
                                  },
                              context_instance=RequestContext(request))

def multiseqalign(request):
    if request.method=="POST":
        seqlst=request.POST.getlist('seqtxt')
        tc=0
        lst=[]
        lstall=[]
        lstjb=[]
        for sl in seqlst:
            lst=list(sl.replace('\r\n',''))
            lstall.append(lst)
        tupx=tuple(lstall)
        lstx=np.column_stack((tupx))
        for lx in lstx:
            i2=""
            lstqc=[]
            i2=''.join(sorted(''.join(list(set(''.join(lx))))))
            lstqc.append(i2)
            print(lstqc)
            for lq in lstqc:
                slq=''.join(lq)
                if slq=='AC' or 'M' in slq:
                    lq='M'
                    tc+=1
                if slq=='GT' or 'K' in slq:
                    lq='K'
                    tc+=1
                if slq=='CT' or 'Y' in slq:
                    lq='Y'
                    tc+=1
                if slq=='AT' or 'W' in slq:
                    lq='W'
                    tc+=1
                if slq=='AG' or 'R' in slq:
                    lq='R'
                    tc+=1
                if slq=='CG' or 'S' in slq:
                    lq='S'
                    tc+=1
                if slq=='ACT' or 'MT' in slq or 'CW' in slq or 'AY' in slq:
                    lq='H'
                    tc+=1
                if slq=='CGT' or 'ST' in slq or 'CK' in slq or 'GY' in slq:
                    lq='B' 
                    tc+=1
                if slq=='ACG' or 'MG' in slq or 'AS' in slq or 'CR' in slq:
                    lq='V'
                    tc+=1
                if slq=='AGT' or 'AK' in slq or 'RT' in slq or 'GW' in slq:
                    lq='D'
                    tc+=1    
                if slq=='ACGT' or 'TV' in slq or 'GH' in slq or 'CD' in slq or 'AB' in slq:
                    lq='N'
                    tc+=1
                lstjb.append(lq)
                msa_seq=''.join(lstjb)
                len_ms=len(msa_seq)
        return render_to_response('msa/msa_result.html',{
            'local':local,
            'thisyear':thisyear,
            'lstall':seqlst,
            'len_ms':len_ms,
            'tc':str(tc),
            'msa_seq':str(msa_seq),
            },context_instance=RequestContext(request))