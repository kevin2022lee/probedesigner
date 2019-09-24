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
        lst=[]
        lstall=[]
        for sl in seqlst:
            lst=list(sl.replace('\r\n',''))
            lstall.append(lst)
        tupx=tuple(lstall)
        lstx=np.column_stack((tupx))
        for lx in lstx:
            i2=""
            lstqc=[]
            for i in ''.join(lx):
                if i not in i2:
                    i2+=i
            lstqc.append(i2)
            for lq in lstqc:
                lstjb=[]
                if ''.join(sorted(lq))=='AC':
                    lq='M'
                if ''.join(sorted(lq))=='GT':
                    lq='K'
                if ''.join(sorted(lq))=='CT':
                    lq='Y'
                if ''.join(sorted(lq))=='AT':
                    lq='W'
                if ''.join(sorted(lq))=='AG':
                    lq='R'
                if ''.join(sorted(lq))=='ACT':
                    lq='H'
                if ''.join(sorted(lq))=='CGT':
                    lq='B' 
                if ''.join(sorted(lq))=='ACG':
                    lq='V'
                if ''.join(sorted(lq))=='AGT':
                    lq='D'    
                if ''.join(sorted(lq))=='ACGT':
                    lq='N'
                lstjb.append(lq)
                
        return render_to_response('msa/msa_result.html',{'local':local,'thisyear':thisyear,'lstjb':lstjb,},context_instance=RequestContext(request))