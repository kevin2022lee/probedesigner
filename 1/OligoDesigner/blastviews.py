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
                if slq=='GT' or 'K' in slq:
                    lq='K'
                if slq=='CT' or 'Y' in slq:
                    lq='Y'
                if slq=='AT' or 'W' in slq:
                    lq='W'
                if slq=='AG' or 'R' in slq:
                    lq='R'
                if slq=='CG' or 'S' in slq:
                    lq='S'
                if slq=='ACT' or 'MT' in slq or 'CW' in slq or 'AY' in slq:
                    lq='H'
                if slq=='CGT' or 'ST' in slq or 'CK' in slq or 'GY' in slq:
                    lq='B' 
                if slq=='ACG' or 'MG' in slq or 'AS' in slq or 'CR' in slq:
                    lq='V'
                if slq=='AGT' or 'AK' in slq or 'RT' in slq or 'GW' in slq:
                    lq='D'    
                if slq=='ACGT' or 'TV' in slq or 'GH' in slq or 'CD' in slq or 'AB' in slq:
                    lq='N'
                lstjb.append(lq)
                msa_seq=''.join(lstjb)
                len_ms=len(msa_seq)
        return render_to_response('msa/msa_result.html',{
            'local':local,
            'thisyear':thisyear,
            'lstall':seqlst,
            'len_ms':len_ms,
            'msa_seq':msa_seq[:110],
            'msa_seq1':msa_seq[110:220],
            'msa_seq2':msa_seq[220:330],
            'msa_seq3':msa_seq[330:440],
            'msa_seq4':msa_seq[440:550],
            'msa_seq5':msa_seq[550:660],
            'msa_seq6':msa_seq[660:770],
            'msa_seq7':msa_seq[770:880],
            'msa_seq8':msa_seq[880:990],
            'msa_seq9':msa_seq[990:1100],
            'msa_seq10':msa_seq[1100:1210],
            'msa_seq11':msa_seq[1210:1320],
            'msa_seq12':msa_seq[1320:1430],
            'msa_seq13':msa_seq[1430:1540],
            'msa_seq14':msa_seq[1540:1650],
            'msa_seq15':msa_seq[1650:1760],
            'msa_seq16':msa_seq[1760:1870],
            'msa_seq17':msa_seq[1870:1980],
            'msa_seq18':msa_seq[1980:2090],
            'msa_seq19':msa_seq[2090:2200],
            'msa_seq20':msa_seq[2200:2310],
            'msa_seq21':msa_seq[2310:2420],
            'msa_seq22':msa_seq[2420:2530],
            'msa_seq23':msa_seq[2530:2640],
            'msa_seq24':msa_seq[2640:2750],
            'msa_seq25':msa_seq[2750:2860],
            'msa_seq26':msa_seq[2860:2970],
            'msa_seq27':msa_seq[2970:3080],
            'msa_seq28':msa_seq[3080:3190],
            'msa_seq29':msa_seq[3190:3300],
            'msa_seq30':msa_seq[3410:3520],
            'msa_seq31':msa_seq[3520:3630],
            'msa_seq32':msa_seq[3630:3740],
            'msa_seq33':msa_seq[3740:3850],
            'msa_seq34':msa_seq[3850:3960],
            'msa_seq35':msa_seq[3960:4070],
            },context_instance=RequestContext(request))