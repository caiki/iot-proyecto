# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User
from django.db.models import Sum,Q,Count
from django.db  import  IntegrityError ,  transaction 
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import json
import sys
import decimal
import math
from django.core import serializers
from Procesos.models import *
from datetime import date,datetime,timedelta,time
import datetime as dtime_
import time
import string
import random



@login_required
@transaction.atomic
def Depositos_view(request):
	exito=''
	pkR= request.POST.get('pkHeart','')
	nroboucher= request.POST.get('fechaTiempo','')
	monto= request.POST.get('frecuenciaC','')
	#concepto= request.POST.get('concepto','')
	#obs=request.POST.get('obs','')
	
	try:
		usr= request.user.username
		if pkR != None and  pkR != '':
			with transaction.atomic():
				monto_deposito = float(monto)
				reporte = TReporteDiario.objects.get(pk=pkR)
				detDeposito = Tdeposito(ReporteDiario=reporte,NroBoucher=nroboucher,Concepto=concepto,Monto=monto_deposito)
				detDeposito.save()
				exito = 'exito'
	except:
		exito= str(sys.exc_info()[1])
	return render_to_response("heart.html",{"resultado":exito},context_instance=RequestContext(request))