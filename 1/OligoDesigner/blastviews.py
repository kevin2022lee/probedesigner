from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect,response
from django.views.decorators.csrf import csrf_protect,csrf_exempt

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
    return render_to_response('msa/msa_result.html',
                              {'local':local,
                               'thisyear':thisyear,
                               'seqlst':seqlst,
                                  },
                              context_instance=RequestContext(request))