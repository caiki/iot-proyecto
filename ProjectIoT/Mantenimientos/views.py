# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from Procesos.models import *
from Mantenimientos.models import *
from Consultas.models import *
from django.http import HttpResponse
from django.db  import  IntegrityError ,  transaction 
import json
import sys
from django.core import serializers

# Create your views here.
@login_required
def autentificar(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/login/')
	else:
		try:
			"""
			if request.user.has_perm("Main.add_oficina"):
				usr = request.user.username
				if Gerente_conf.objects.filter(id_gerente__usuario=usr,subGerente="si").exists():
					return HttpResponseRedirect('/sistem/Movimientos_admin_tem/')
				else:
					return HttpResponseRedirect('/sistem/Personales/')
			"""
			#else:
			usr = request.user.username
			#C= Cajas.objects.get(id_usuario__usuario=usr)
			#if C.estado and C.id_oficina.estado_oficina and C.id_usuario.estado:
			return HttpResponseRedirect('/Bienvenida/')
			#else:
			#	return HttpResponseRedirect('/cerrar/')
		except:
			return HttpResponseRedirect('/cerrar/')

@login_required
def Bienvenida_view(request):
	exito=''
	pke= request.POST.get('estacion')
	try:
		usr= request.user.username
		if pke != None and  pke != '':
			Estacion= Grifo.objects.get(pk=pke)
			with transaction.atomic():
				if Inicio.objects.all().count() == 0:
					ini= Inicio(Grifo=Estacion)
					ini.save()
				else:
					pk=''
					if TReporteDiario.objects.filter(Grifo=Estacion).exists():
						Ureporte= TReporteDiario.objects.filter(Grifo=Estacion).latest("pk")
						pk=Ureporte.pk
					Inicio.objects.all().update(Grifo=Estacion,aux1=pk)

				exito='exito'
				return HttpResponseRedirect('/NuevoReporte/')
		else:
			return render_to_response('Bienvenida.html',{"resultado":exito},context_instance=RequestContext(request))
	except:
		exito= str(sys.exc_info()[1])
		return render_to_response('Bienvenida.html',{"resultado":exito},context_instance=RequestContext(request))

def AgregarHeart_ajax_view(request):
	data=''
	if request.is_ajax:
		FechaTiempo=request.GET.get('FechaTiempo')
		Beat=request.GET.get('Beat')
		try:
			with transaction.atomic():
				if FechaTiempo != None and FechaTiempo !="":
					est = THeart(FechaTiempo=FechaTiempo,Beat=Beat)
					est.save()
					data="exito"
				else:
					data='complete todos los campos'
		except IntegrityError:
			data='fail'
		except:
			data='fail'+ str(sys.exc_info()[1]) + FechaTiempo + "//" + Beat
	else:
		data="fail" 
	mimetype="text"
	return HttpResponse(data,mimetype)

@login_required
def Inicio_view(request):
	return render_to_response('inicio.html',context_instance=RequestContext(request))