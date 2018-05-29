from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db.models import Sum,Q
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db  import  IntegrityError ,  transaction 
import json
import sys
from django.core import serializers
from Procesos.models import *
from datetime import datetime, date, time, timedelta
import time
def data_global(request):
	usuario=''
	try:
		usuario= request.user.username
		grifo='-----'
		id_grifo='-----'
		admin='-----'
		RfechaI=''
		RfechaF=''
		pkR=''
		if Inicio.objects.all().exists():
			ui=Inicio.objects.all().latest("pk")
			grifo=ui.Grifo.NombreEstacion
			id_grifo=ui.Grifo.pk
			admin=ui.Grifo.Administrador
			if ui.aux1 !='' and ui.aux1!= None:
				repor= TReporteDiario.objects.get(pk=ui.aux1)
				RfechaI=str(repor.FechaInicial.strftime("%d-%m-%Y"))
				RfechaF=str(repor.FechaFinal.strftime("%d-%m-%Y"))
				pkR=repor.pk
		dict = {
			'usuario': usuario,'grifo':grifo,'pkGrifo':id_grifo,'admin':admin,'RfI':RfechaI,'RfF':RfechaF,'pkR':pkR
		}
	except:
		dict = {
			'usuario': "",'fail':str(sys.exc_info()[1])
		}
	return dict