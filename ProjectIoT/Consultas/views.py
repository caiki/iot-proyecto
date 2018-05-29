# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.db.models import Sum,Q,Avg,Count
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db  import  IntegrityError ,  transaction 
import json
import sys
from django.core import serializers
from Procesos.models import *
from Mantenimientos.models import *
from Consultas.models import *
from datetime import date, time, timedelta
import time
import datetime
import calendar
from django.db.models import Q

@login_required
def listado_Clientes_view(request):
	if request.is_ajax:
		pag=request.GET.get('pg','')
		pg= 1
		if pag !='':
			pg= int(pag)
		desde= (pg-1)*20
		hasta= pg*20
		try:
			consulta=list(TTitular.objects.all().values('pk','Nombre','DocID','Debito','Credito').exclude(Q(Nombre="MASTER CARD")| Q(Nombre="VISANET")))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['Nombre']
				dato['doc']=obj['DocID']
				dato['credito']=round(float(obj['Credito']),2)
				dato['debito']=round(float(obj['Debito']),2)
				dato['saldo']=round(float(obj['Debito'])-float(obj['Credito']),2)
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Combustibles_view(request):
	if request.is_ajax:
		try:
			consulta=list(TCombustible.objects.all().values('pk','NombreCombustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreCombustible']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Tarjetas_view(request):
	if request.is_ajax:
		try:
			#consulta=list(TTitular.objects.all().values('pk','Nombre').filter(Nombre="VISANET"|Nombre="MASTER CARD"))
			consulta=list(TTitular.objects.filter(Q(Nombre="MASTER CARD")| Q(Nombre="VISANET")).values('pk','Nombre'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['Nombre']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Estaciones_view(request):
	if request.is_ajax:
		try:
			consulta=list(Grifo.objects.all().values('pk','NombreEstacion','Administrador'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreEstacion']
				dato['admin']=obj['Administrador']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)


@login_required
def listado_Surtidores_view(request):
	pkEstacion=request.GET.get('grifo')
	if request.is_ajax:
		try:
			consulta=list(Surtidor.objects.filter(Grifo=pkEstacion).values('pk','NombreSurtidor'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreSurtidor']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Manhguera_view(request):
	pkSurtidor=request.GET.get('surtidor')
	if request.is_ajax:
		try:
			consulta=list(TManguera.objects.filter(Surtidor=pkSurtidor).values('pk','NombreManguera','Combustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreManguera']
				comb= TCombustible.objects.get(pk=obj['Combustible'])
				dato['combustible']= comb.NombreCombustible
				dato['pk_comb']= obj['Combustible']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)
"""
@login_required
def listado_Mangueras_tabla_view(request):
	pkSurtidor=request.GET.get('surtidor')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TManguera.objects.filter(Surtidor=pkSurtidor).values('pk','NombreManguera','Combustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreManguera']
				precio= PrecioCombustible.objects.get(Combustible=obj['Combustible'],ReporteDiario=pkReporte)
				dato['precio']= float(precio.PrecioActual)
				dato['diaI']=''
				if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
					Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
					dato['diaI']=float(Ulectura.ValorContometroFinal1)
				
				dato['diaI2']=''
				if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
					Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
					dato['diaI2']=float(Ulectura.ValorContometroFinal2)
				
				dato['diaF']=''
				dato['nocheF']=''
				dato['pkLectura']=''
				if LecturaContometro.objects.filter(ReporteDiario=pkReporte,Manguera=obj['pk']).exists():
					lect= LecturaContometro.objects.get(ReporteDiario=pkReporte,Manguera=obj['pk'])
					dato['diaF']=float(lect.ValorContometroFinal1)
					dato['nocheF']=float(lect.ValorContometroFinal2)
					dato['pkLectura']=lect.pk
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)
"""

@login_required
def listado_Mangueras_tabla_view(request):
	pkSurtidor=request.GET.get('surtidor')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TManguera.objects.filter(Surtidor=pkSurtidor).values('pk','NombreManguera','Combustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreManguera']
				print(dato['pk'])
				print(dato['nombre'])
				print(obj['Combustible'])
				print(pkReporte)
				precio= PrecioCombustible.objects.get(Combustible=obj['Combustible'],ReporteDiario=pkReporte)
				dato['precio']= float(precio.PrecioActual)
				dato['diaI']=''
				if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
					Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
					dato['diaI']=float(Ulectura.ValorContometroFinal2)
				dato['diaF']=''
				dato['nocheF']=''
				dato['pkLectura']=''
				if LecturaContometro.objects.filter(ReporteDiario=pkReporte,Manguera=obj['pk']).exists():
					lect= LecturaContometro.objects.get(ReporteDiario=pkReporte,Manguera=obj['pk'])
					dato['diaF']=float(lect.ValorContometroFinal1)
					dato['nocheF']=float(lect.ValorContometroFinal2)
					dato['pkLectura']=lect.pk
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_movimientos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TMovimientoVista.objects.filter(ReporteDiario=pkReporte).values('pk','Motivo','IngresoTransferencia','IngresoTransferenciaContable','Tanque_id','Titular_id','Observacion'))
			lista=[]
			total=0.0
			for obj in consulta:
				dato={}
				tanque=Tanque.objects.get(pk=obj['Tanque_id'])
				dato['nombreTanque']=tanque.Nombre
				dato['pk']=obj['pk']
				dato['motivo']=obj['Motivo']
				dato['ingresocontable']=round(float(obj['IngresoTransferenciaContable']),2)
				#dato['punitario']=round(float(obj['Punitario']),2)
				dato['observacion']=obj['Observacion']
				if obj['Titular_id']!=None:
					titular=TTitular.objects.get(pk=obj['Titular_id'])
					dato['titular']=titular.Nombre
				else:
					dato['titular']='GRIFO'
				dato['ingresoreal']=round(float(obj['IngresoTransferencia']),2)
				if obj['Motivo']=='COMPRA' or obj['Motivo']=='DEVOLUCION' or obj['Motivo']==None:
					total=round(total+dato['ingresoreal'],2)
				else:
					total=round(total-dato['ingresoreal'],2)

				lista.append(dato)
			lista.append({'totalMovimientosreal':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)


@login_required
def listado_creditos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleCreditos.objects.filter(ReporteDiario=pkReporte).values('pk','NroVale','ReporteDiario','Titular','Concepto','Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				titu=TTitular.objects.get(pk=obj['Titular'])
				if titu.Nombre != "VISANET" and titu.Nombre != "MASTER CARD":
					dato['titular']=titu.Nombre[0:26]
					dato['pk']=obj['pk']
					dato['nroVale']=obj['NroVale']
					dato['reporte']=obj['ReporteDiario']
					dato['pktitular']=obj['Titular']
					dato['concepto']=obj['Concepto']
					dato['monto']=round(float(obj['Monto']),2)
					total=round(total+dato['monto'],2)
					lista.append(dato)
			lista.append({'totalCreditos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_compras_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TCompra.objects.values('FechaCompra','NroDocumento','idMovimientoVista','TransporteGalon','Punitario','Igv','Percepcion'))
			lista=[]
			total=0
			PrecioCompra = 0
			for obj in consulta:
				dato={}
				MovimientoVista=TMovimientoVista.objects.get(pk=obj['idMovimientoVista'])
				dato['FechaCompra']=str(obj['FechaCompra'])
				dato['NroDocumento']=obj['NroDocumento']
				oTanque = Tanque.objects.get(pk=int(str(MovimientoVista.Tanque)))
				dato['Tanque'] = oTanque.Nombre 
				dato['GalonesContable'] = str(round(MovimientoVista.IngresoTransferencia,2))
				dato['Punitario'] = str(obj['Punitario'])
				PrecioCompra = obj['Punitario']*MovimientoVista.IngresoTransferencia
				dato['PrecioCompra'] = str(round(PrecioCompra,2))
				dato['CompraIgvPercepcion'] = str(round(PrecioCompra*(1+obj['Igv']/100)*(1+obj['Percepcion']/100),2))
				lista.append(dato)
				#total=round(total+dato['monto'],2)
			
			#lista.append({'totalCreditos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_creditos_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleCreditos.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','NroVale','ReporteDiario','Titular','Concepto','Monto'))
			lista=[]
			for obj in consulta:
				dato={}
				titu=TTitular.objects.get(pk=obj['Titular'])
				if titu.Nombre != "VISANET" and titu.Nombre != "MASTER CARD":
					dato['pk']=obj['pk']
					dato['nroVale']=obj['NroVale']
					dato['reporte']=obj['ReporteDiario']
					dato['pktitular']=obj['Titular']
					dato['titular']=titu.Nombre
					dato['concepto']=obj['Concepto']
					dato['monto']=round(float(obj['Monto']),2)
					lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_descuentos_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleDescuento.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','NroVale','ReporteDiario','Titular','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['pktitular']=obj['Titular']
				titu=TTitular.objects.get(pk=obj['Titular'])
				dato['titular']=titu.Nombre
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalDescuentos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_gastos_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleGastos.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','NroVale','ReporteDiario','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalGastos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Serafin_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleSerafin.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','NroVale','ReporteDiario','Cantidad','Combustible','Observacion','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['observacion']=obj['Observacion']
				dato['pkcombustible']=obj['Combustible']
				ncombustible=TCombustible.objects.get(pk=obj['Combustible'])
				dato['combustible']=ncombustible.NombreCombustible
				dato['cantidad']=round(float(obj['Cantidad']),2)
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalSerafin':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_depositos_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(Tdeposito.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','NroBoucher','ReporteDiario','Concepto','Monto'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroBoucher']=obj['NroBoucher']
				dato['reporte']=obj['ReporteDiario']
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_pagos_view(request):
	pg=request.GET.get('pg')
	pkGrifo=request.GET.get('pkGrifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TPagos.objects.filter(ReporteDiario=pkReporte,ReporteDiario__Grifo=pkGrifo).values('pk','ReporteDiario','Titular','Concepto','MontoAmortizado'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['reporte']=obj['ReporteDiario']
				titu=TTitular.objects.get(pk=obj['Titular'])
				dato['titular']=titu.Nombre
				dato['pktitular']=obj['Titular']
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['MontoAmortizado']),2)
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_PrecioCombustible_view(request):
	pkReport=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(PrecioCombustible.objects.filter(ReporteDiario=pkReport).values('pk','Combustible','PrecioAnterior','PrecioActual'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				comb= TCombustible.objects.get(pk=obj['Combustible'])
				dato['pkcombustible']=obj['Combustible']
				dato['combustible']=comb.NombreCombustible
				dato['precioActual']=float(obj['PrecioActual'])
				dato['precioAnterior']=float(obj['PrecioAnterior'])
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Tanques_ajax_view(request):
	pkEstacion=request.GET.get('grifo')
	if request.is_ajax:
		try:
			consulta=list(Tanque.objects.filter(Grifo=pkEstacion).values('pk','Nombre','Combustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['Nombre']
				dato['pkCombustible']=obj['Combustible']
				combu= TCombustible.objects.get(pk=obj['Combustible'])
				dato['combustible']=combu.NombreCombustible
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Tanques_tabla_view(request):
	pkGrifo=request.GET.get('grifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(Tanque.objects.filter(Grifo=pkGrifo).values('pk','Nombre','Combustible'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['Nombre']
				precio= PrecioCombustible.objects.get(Combustible=obj['Combustible'],ReporteDiario=pkReporte)
				dato['precio']= float(precio.PrecioActual)
				dato['saldoAnt']=''

				if TSaldoCombustible.objects.filter(ReporteDiario__lt=pkReporte,Tanque=obj['pk']).exists():
					UMovi= TSaldoCombustible.objects.filter(ReporteDiario__lt=pkReporte,Tanque=obj['pk']).latest("pk")
					dato['saldoAnt']=float(UMovi.SaldoActual)
				dato['saldoAct']=''
				dato['ingresoTra']=''
				dato['pkMovi']=''

				if TSaldoCombustible.objects.filter(ReporteDiario=pkReporte,Tanque=obj['pk']).exists():
					lect= TSaldoCombustible.objects.get(ReporteDiario=pkReporte,Tanque=obj['pk'])
					dato['saldoAct']=float(lect.SaldoActual)
					dato['pkMovi']=lect.pk

				query = list(TMovimientoVista.objects.filter(ReporteDiario=pkReporte,Tanque=obj['pk']).values('pk','IngresoTransferencia','Motivo'))
				if query:
					tot = 0
					for objmov in query:
						if objmov['Motivo']=='COMPRA' or objmov['Motivo']=='DEVOLUCION' or objmov['Motivo']==None:
							tot = tot + float(objmov['IngresoTransferencia'])
						else:
							tot = tot - float(objmov['IngresoTransferencia'])
					dato['ingresoTra'] = tot


				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_diario_ajax_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			reporte=TReporteDiario.objects.get(pk=pkReporte)
			dato={}
			dato['pk']=reporte.pk
			dato['fechaIni']=str(reporte.FechaInicial.strftime("%Y-%m-%d"))
			dato['fechaFin']=str(reporte.FechaFinal.strftime("%Y-%m-%d"))
			dato['griferos']=reporte.Griferos
			dato['estacion']=reporte.Grifo.NombreEstacion
			dato['admin']=reporte.Grifo.Administrador
			dato['obs']=reporte.Observacion
			dato['monto_griferos']=float(reporte.DepositoBancos)
			dato['saldoCredito']=float(reporte.SaldoCredito)
			dato['saldoGasto']=float(reporte.SaldoGastos)
			dato['saldoGastoAnt']=0
			dato['saldoCreditoAnt']=0
			if TReporteDiario.objects.filter(pk__lt=pkReporte,Grifo=reporte.Grifo.pk).exists():
				UReporte=TReporteDiario.objects.filter(pk__lt=pkReporte,Grifo=reporte.Grifo.pk).latest("pk")
				dato['saldoGastoAnt']=float(UReporte.SaldoGastos)
				dato['saldoCreditoAnt']=float(UReporte.SaldoCredito)
			lista_surtidor=[]
			surtidores = list(Surtidor.objects.filter(Grifo=reporte.Grifo.pk).values('pk','NombreSurtidor'))
			for obj in surtidores:
				aux={}
				aux['pk']=obj['pk']
				aux['surtifor']=obj['NombreSurtidor']
				lista_surtidor.append(aux);
			dato['surtidores']=lista_surtidor
			data= json.dumps(dato)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

def esReal(t):
	try:
		f=float(t)
		return True
	except:
		return False

@login_required
def lectura_Xreporte_ajax_view(request):
	pkReporte=request.GET.get('pkReporte')
	pkSurtidor=request.GET.get('surtidor')
	if request.is_ajax:
		try:
			consulta=list(TManguera.objects.filter(Surtidor=pkSurtidor).values('pk','NombreManguera','Combustible'))
			lista=[]
			totalV=0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['NombreManguera']
				precio= PrecioCombustible.objects.get(Combustible=obj['Combustible'],ReporteDiario=pkReporte)
				dato['precio']= float(precio.PrecioActual)
				dato['diaI']=''
				if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
					Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
					dato['diaI']=float(Ulectura.ValorContometroFinal2)
				dato['diaF']=''
				dato['nocheF']=''
				dato['pkLectura']=''
				if LecturaContometro.objects.filter(ReporteDiario=pkReporte,Manguera=obj['pk']).exists():
					lect= LecturaContometro.objects.get(ReporteDiario=pkReporte,Manguera=obj['pk'])
					dato['diaF']=float(lect.ValorContometroFinal1)
					dato['nocheF']=float(lect.ValorContometroFinal2)
					dato['pkLectura']=lect.pk
				dato['cantGa1']= ''
				dato['cantGa2']= ''
				dato['totalGa']= ''
				dato['venta']= ''
				if esReal(dato['diaI']) and esReal(dato['diaF']) and esReal(dato['nocheF']):
					aux1= dato['diaF'] - dato['diaI']
					aux2= dato['nocheF'] - dato['diaF']
					dato['cantGa1']=round(aux1,2)
					dato['cantGa2']=round(aux2,2)
					dato['totalGa']=round(aux2+aux1,2)
					dato['venta']=round((aux2+aux1)* dato['precio'],2)
					totalV=totalV+dato['venta']
					totalV=round(totalV,2)
				lista.append(dato)
			lista.append({'totalVenta':totalV})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)


@login_required
def listado_tarjetas_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			#consulta=list(TTitular.objects.filter(Q(Nombre="MASTER CARD")| Q(Nombre="VISANET")).values('pk','Nombre'))
			consulta=list(TDetalleCreditos.objects.filter(ReporteDiario=pkReporte).values('pk','NroVale','ReporteDiario','Titular','Concepto','Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				titu=TTitular.objects.get(pk=obj['Titular'])
				if titu.Nombre == "VISANET" or titu.Nombre == "MASTER CARD":
					dato['titular']=titu.Nombre[0:26]
					dato['pk']=obj['pk']
					dato['nroVale']=obj['NroVale']
					dato['reporte']=obj['ReporteDiario']
					dato['pktitular']=obj['Titular']
					dato['concepto']=obj['Concepto']
					dato['monto']=round(float(obj['Monto']),2)
					total=round(total+dato['monto'],2)
					lista.append(dato)
			lista.append({'totalCreditos':total})
			data= json.dumps(lista)
			print(data)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)


@login_required
def listado_descuentos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			#consulta=list(TTitular.objects.filter(Q(Nombre="MASTER CARD")| Q(Nombre="VISANET")).values('pk','Nombre'))
			consulta=list(TDetalleDescuento.objects.filter(ReporteDiario=pkReporte).values('Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalDescuentos':total})
			data= json.dumps(lista)
			print(data)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_serafin_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			#consulta=list(TTitular.objects.filter(Q(Nombre="MASTER CARD")| Q(Nombre="VISANET")).values('pk','Nombre'))
			consulta=list(TDetalleSerafin.objects.filter(ReporteDiario=pkReporte).values('Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalDescuentos':total})
			data= json.dumps(lista)
			print(data)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_gastos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TDetalleGastos.objects.filter(ReporteDiario=pkReporte).values('pk','NroVale','ReporteDiario','Concepto','Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['concepto']=obj['Concepto'][0:31]
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalGastos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_depositos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(Tdeposito.objects.filter(ReporteDiario=pkReporte).values('pk','NroBoucher','ReporteDiario','Concepto','Monto'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroBoucher']=obj['NroBoucher']
				dato['reporte']=obj['ReporteDiario']
				dato['concepto']=obj['Concepto'][0:31]
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalDepositos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

#<<<<<<< HEAD
#def calcular_monto_contometro(pkCombustible,pkReporte,pkGrifo):
#=======
def calcular_monto_contometro(pkCombustible,pkReporte,pkGrifo,pkTanque):
	total=0
	total_dia=0
	total_noche=0
	precio=0
	p= PrecioCombustible.objects.get(Combustible=pkCombustible,ReporteDiario=pkReporte)
	precio= float(p.PrecioActual)
	consulta=list(TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible,Tanque=pkTanque).values('pk','NombreManguera','Combustible'))
	"""
<<<<<<< HEAD
	consulta=list(TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible).values('pk','NombreManguera','Combustible'))
=======
	consulta=[]
	if not TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible,Tanqu=pkTanque).exists():
		consulta=list(TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible,Tanque="n").values('pk','NombreManguera','Combustible'))
	else:
		consulta=list(TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible,Tanque=pkTanque).values('pk','NombreManguera','Combustible'))
>>>>>>> 371d9c22e7544096615209f22653858214f756b9
	"""
	for obj in consulta:
		diai=''
		diaf=''
		nochef=''
		if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
			Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
			diai=float(Ulectura.ValorContometroFinal2)
		if LecturaContometro.objects.filter(ReporteDiario=pkReporte,Manguera=obj['pk']).exists():
			lect= LecturaContometro.objects.get(ReporteDiario=pkReporte,Manguera=obj['pk'])
			diaf=float(lect.ValorContometroFinal1)
			nochef=float(lect.ValorContometroFinal2)
		if esReal(diai) and esReal(diaf) and esReal(nochef):
			auxto= (nochef - diai)*precio
			auxdia= (diaf - diai)*precio
			auxnoche= (nochef - diaf)*precio
			total=total+auxto
			total_dia=total_dia+auxdia
			total_noche=total_noche+auxnoche
	return total,total_dia,total_noche

"""  Tio Lucho
#<<<<<<< HEAD
#def calcular_monto_contometro(pkCombustible,pkReporte,pkGrifo):
#=======
def calcular_monto_contometro(pkCombustible,pkReporte,pkGrifo,pkTanque):
	total=0
	total_dia=0
	total_noche=0
	precio=0
	p= PrecioCombustible.objects.get(Combustible=pkCombustible,ReporteDiario=pkReporte)
	precio= float(p.PrecioActual)
	consulta=list(TManguera.objects.filter(Surtidor__Grifo=pkGrifo,Combustible=pkCombustible,Tanque=pkTanque).values('pk','NombreManguera','Combustible'))

	for obj in consulta:
		diai=''
		diaf=''
		nochef=''
		if LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).exists():
			Ulectura= LecturaContometro.objects.filter(ReporteDiario__lt=pkReporte,Manguera=obj['pk']).latest("pk")
			diai=float(Ulectura.ValorContometroFinal1)
			diai2=float(Ulectura.ValorContometroFinal2)
		if LecturaContometro.objects.filter(ReporteDiario=pkReporte,Manguera=obj['pk']).exists():
			lect= LecturaContometro.objects.get(ReporteDiario=pkReporte,Manguera=obj['pk'])
			diaf=float(lect.ValorContometroFinal1)
			nochef=float(lect.ValorContometroFinal2)
		if esReal(diai) and esReal(diaf) and esReal(nochef):
			#auxto= (nochef - diai)*precio
			#auxto= (diaf - diai)*precio
			#auxdia= (diaf - diai)*precio
			auxdia=(diaf - diai)*precio
			#auxnoche= (nochef - diai2)*precio
			auxnoche=(nochef - diai2)*precio
			auxto= auxdia+auxnoche
			#print(auxto/precio)
			total=total+auxto
			total_dia=0
			#total_dia=total_dia+auxdia
			total_noche=0
	return total,total_dia,total_noche
"""

@login_required
def Movimiento_vista_reporte_view(request):
	pkGrifo=request.GET.get('grifo')
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(Tanque.objects.filter(Grifo=pkGrifo).values('pk','Nombre','Combustible'))
			lista=[]
			TsaldoAnt=0
			TingresoTra=0
			TsaldoAct=0
			TventaGln=0
			Ttotal=0
			#precio e ingresoTra es igual  para movimiento contable
			Tmc_saldoAnt=0
			Tmc_saldoAct=0
			Tmc_ventaGln=0
			Tmc_total=0
			Tmc_total_dia=0
			Tmc_total_noche=0
			Tdif=0
			TsaldoAcu=0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nombre']=obj['Nombre']
				precio= PrecioCombustible.objects.get(Combustible=obj['Combustible'],ReporteDiario=pkReporte)
				dato['precio']= float(precio.PrecioActual)
				dato['saldoAnt']=''
				dato['mc_saldoAnt']=''
				if TSaldoCombustible.objects.filter(ReporteDiario__lt=pkReporte,Tanque=obj['pk']).exists():
					UMovi= TSaldoCombustible.objects.filter(ReporteDiario__lt=pkReporte,Tanque=obj['pk']).latest("pk")
					dato['saldoAnt']=float(UMovi.SaldoActual)
					dato['mc_saldoAnt']=float(UMovi.SaldoActualMovContable)
					TsaldoAnt= round(TsaldoAnt+dato['saldoAnt'],2)
					Tmc_saldoAnt= round(Tmc_saldoAnt+dato['mc_saldoAnt'],2)
				dato['saldoAct']=''
				dato['ingresoTra']=''
				dato['pkMovi']=''
				
				query = list(TMovimientoVista.objects.filter(ReporteDiario=pkReporte,Tanque=obj['pk']).values('pk','IngresoTransferencia','Motivo'))
				if query:
					tot = 0
					for objmov in query:
						if objmov['Motivo']=='COMPRA' or objmov['Motivo']=='DEVOLUCION' or objmov['Motivo']==None:
							tot = tot + float(objmov['IngresoTransferencia'])
						else:
							tot = tot - float(objmov['IngresoTransferencia'])
					dato['ingresoTra'] = tot
					TingresoTra= round(TingresoTra + dato['ingresoTra'],2)


				if TSaldoCombustible.objects.filter(ReporteDiario=pkReporte,Tanque=obj['pk']).exists():
					lect= TSaldoCombustible.objects.get(ReporteDiario=pkReporte,Tanque=obj['pk'])
					dato['saldoAct']=float(lect.SaldoActual)
					dato['pkMovi']=lect.pk
					TsaldoAct=round(TsaldoAct + dato['saldoAct'],2)
				
				dato['ventaGln']=''
				dato['total']=''
				dato['mc_total']=''
				dato['mc_ventaGln']=''
				dato['mc_saldoAct']=''
				dato['mc_dif']=''
				dato['saldoAcu']=''
				if esReal(dato['saldoAnt']) and esReal(dato['saldoAct']) and esReal(dato['ingresoTra']):
					aux= dato['saldoAnt'] +dato['ingresoTra']-dato['saldoAct']
					dato['ventaGln']=round(aux,2)
					dato['total']=round(aux*dato['precio'],2)
#					aux1,aux2,aux3=calcular_monto_contometro(obj['Combustible'],pkReporte,pkGrifo)
					aux1,aux2,aux3=calcular_monto_contometro(obj['Combustible'],pkReporte,pkGrifo,obj['pk'])
					dato['mc_total']=round(aux1,2)
					dato['mc_ventaGln']=round(dato['mc_total']/dato['precio'],2)
					dato['mc_saldoAct']=round(dato['mc_saldoAnt']+dato['ingresoTra']-dato['mc_ventaGln'],2)
					dato['mc_dif']=round(dato['mc_ventaGln'] -dato['ventaGln'],2)
					dato['saldoAcu']= round(dato['saldoAct'] - dato['mc_saldoAct'],2)
					TventaGln= round(TventaGln+aux,2)
					Tmc_ventaGln= round(Tmc_ventaGln+dato['mc_ventaGln'],2)
					Tmc_saldoAct= round(Tmc_saldoAct+dato['mc_saldoAct'],2)
					Tmc_total= round(Tmc_total+dato['mc_total'],2)
					Tmc_total_dia= round(Tmc_total_dia+aux2,2)
					Tmc_total_noche= round(Tmc_total_noche+ aux3,2)
					Ttotal= round(Ttotal+dato['total'],2)
					Tdif= round(Tdif+dato['mc_dif'],2)
					TsaldoAcu= round(TsaldoAcu+dato['saldoAcu'],2)
				lista.append(dato)
			lista.append({'TsaldoAnt':TsaldoAnt,'TsaldoAct':TsaldoAct,'TingresoTra':TingresoTra,'TventaGln':TventaGln,'Ttotal':Ttotal,'Tmc_total':Tmc_total,'Tmc_saldoAnt':Tmc_saldoAnt,'Tmc_ventaGln':Tmc_ventaGln,'Tmc_saldoAct':Tmc_saldoAct,'Tdif':Tdif,'TsaldoAcu':TsaldoAcu,'Tmc_total_dia':Tmc_total_dia,'Tmc_total_noche':Tmc_total_noche})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)


@login_required
def listado_pagos_reporte_view(request):
	pkReporte=request.GET.get('pkReporte')
	if request.is_ajax:
		try:
			consulta=list(TPagos.objects.filter(ReporteDiario=pkReporte).values('pk','Concepto','MontoAmortizado','Titular'))
			lista=[]
			total=0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['concepto']=obj['Concepto']
				titu=TTitular.objects.get(pk=obj['Titular'])
				dato['titular']=titu.Nombre[0:18]+"..."
				dato['monto']=round(float(obj['MontoAmortizado']),2)
				total=total+dato['monto']
				lista.append(dato)
			lista.append({'totalPagos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_reportes_view(request):
	return render_to_response('ListadoReportes.html',context_instance=RequestContext(request))

@login_required
def listado_reportes_ajax_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	if request.is_ajax:
		try:
			consulta=list(TReporteDiario.objects.filter(Grifo=pkGrifo).order_by('-pk').values('pk','FechaInicial','FechaFinal','Griferos','Grifo','DepositoBancos','SaldoCredito','SaldoGastos','Observacion'))
			lista=[]
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['desde']=str(obj['FechaInicial'].strftime("%d-%m-%Y"))
				dato['hasta']=str(obj['FechaFinal'].strftime("%d-%m-%Y"))
				dato['griferos']=obj['Griferos']
				g=Grifo.objects.get(pk=obj['Grifo'])
				dato['Grifo']=g.NombreEstacion
				dato['montoGri']=round(float(obj['DepositoBancos']),2)
				dato['saldoGa']=round(float(obj['SaldoGastos']),2)
				dato['saldoCre']=round(float(obj['SaldoCredito']),2)
				dato['obs']=obj['Observacion']
				lista.append(dato)
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

#reportes mensuales
@login_required
def reporte_sa_compra_mes_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m).latest('FechaFinal')
			pre_combustibles = list(PrecioCombustible.objects.filter(ReporteDiario=reporte.pk).values('Combustible','PrecioActual'))
			lista=[]
			total=0
			for obj in pre_combustibles:
				comb = TCombustible.objects.get(pk=obj['Combustible'])
				dato={}
				dato['prod']=comb.NombreCombustible
				lec = LecturaContometro.objects.filter(ReporteDiario=reporte.pk,Manguera__Combustible=obj['Combustible']).aggregate(galones=Sum('ValorContometroFinal2'))
				dato['galones_sa']=0
				if lec['galones']!=None:
					dato['galones_sa']= float(lec['galones'])
				dato['ppv'] = float(obj['PrecioActual'])
				dato['subto_sa']= round(float(dato['galones_sa']*dato['ppv']),2)
				total=total+dato['subto_sa']
				lista.append(dato)
			lista.append({'total_sa':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_creditos_mes_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			#reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m)
			creditos = list(TDetalleCreditos.objects.exclude(Titular__Nombre='VISANET').exclude(Titular__Nombre='MARTER CARD').filter(ReporteDiario__Grifo=pkEstacion,ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m).values('Titular').annotate(Monto=Sum('Monto')).order_by('-Monto'))
			lista=[]
			total=0
			print len(creditos)
			for obj in creditos:
				pago = TPagos.objects.filter(ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular=obj['Titular']).aggregate(Monto=Sum('MontoAmortizado'))
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['nombre']= titular.Nombre[:30]
				m_pago=0
				if pago['Monto'] != None:
					m_pago=float(pago['Monto'])
				dato['credito'] = float(obj['Monto'])-m_pago
				total= total+dato['credito']
				lista.append(dato)
			lista.append({'totalCredito':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_gastos_mes_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	filtro=request.GET.get('filtro')
	f1=request.GET.get('F1')
	m = f1.split('-')[1]
	y = f1.split('-')[0]
	f2=request.GET.get('F2')
	if request.is_ajax:
		try:
			consulta=list(TDetalleGastos.objects.filter(ReporteDiario__Grifo=pkGrifo,ReporteDiario__FechaFinal__month=m,ReporteDiario__FechaFinal__year=y).values('pk','NroVale','ReporteDiario','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=round(total+dato['monto'],2)
				lista.append(dato)
			lista.append({'totalGastos':total})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_gastos_reporte_mes_view(request):
	return render_to_response('reporteGastos.html',context_instance=RequestContext(request))


@login_required
def listado_creditos_reporte_mes_view(request):
	return render_to_response('reporteCreditos.html',context_instance=RequestContext(request))

@login_required
def listado_credito_mes_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	filtro=request.GET.get('filtro')
	f1=request.GET.get('F1')
	m = f1.split('-')[1]
	y = f1.split('-')[0]
	f2=request.GET.get('F2')
	if request.is_ajax:
		try:
			consulta=list(TDetalleCreditos.objects.filter(ReporteDiario__Grifo=pkGrifo,ReporteDiario__FechaFinal__month=m,ReporteDiario__FechaFinal__year=y).exclude(Titular__Nombre='VISANET').exclude(Titular__Nombre='MARTER CARD').values('pk','NroVale','Titular','ReporteDiario','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['titular']=titular.Nombre
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=total+dato['monto']
				lista.append(dato)
			lista.append({'totalCreditos':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_creditos_mes_cliente_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			#reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m)
			creditos = list(TDetalleCreditos.objects.exclude(Titular__Nombre='VISANET').exclude(Titular__Nombre='MARTER CARD').filter(ReporteDiario__Grifo=pkEstacion,ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m).values('Titular').annotate(Monto=Sum('Monto')).order_by('-Monto'))
			lista=[]
			total=0
			print len(creditos)
			for obj in creditos:
				#pago = TPagos.objects.filter(ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular=obj['Titular']).aggregate(Monto=Sum('MontoAmortizado'))
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['nombre']= titular.Nombre[:30]

				#m_pago=0
				#if pago['Monto'] != None:
				#	m_pago=float(pago['Monto'])
				dato['credito'] = float(obj['Monto'])#-m_pago
				total= total+dato['credito']
				lista.append(dato)
			lista.append({'totalCredito':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

#tarjetas
@login_required
def listado_Tarjeta_mes_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	filtro=request.GET.get('filtro')
	f1=request.GET.get('F1')
	m = f1.split('-')[1]
	y = f1.split('-')[0]
	f2=request.GET.get('F2')
	if request.is_ajax:
		try:
			consulta=list(TDetalleCreditos.objects.filter(ReporteDiario__Grifo=pkGrifo,ReporteDiario__FechaFinal__month=m,ReporteDiario__FechaFinal__year=y,Titular__Nombre__in=['VISANET','MARTER CARD']).values('pk','NroVale','Titular','ReporteDiario','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['tarjeta']=titular.Nombre
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=total+dato['monto']
				lista.append(dato)
			lista.append({'totalTarjetas':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_tarjeta_mes_tipo_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			#reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m)
			creditos = list(TDetalleCreditos.objects.filter(ReporteDiario__Grifo=pkEstacion,ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular__Nombre__in=['VISANET','MARTER CARD']).values('Titular').annotate(Monto=Sum('Monto')).order_by('-Monto'))
			lista=[]
			total=0
			print len(creditos)
			for obj in creditos:
				#pago = TPagos.objects.filter(ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular=obj['Titular']).aggregate(Monto=Sum('MontoAmortizado'))
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['nombre']= titular.Nombre[:30]

				#m_pago=0
				#if pago['Monto'] != None:
				#	m_pago=float(pago['Monto'])
				dato['credito'] = float(obj['Monto'])#-m_pago
				total= total+dato['credito']
				lista.append(dato)
			lista.append({'totalTarjeta':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_tarjeta_reporte_mes_view(request):
	return render_to_response('reporteTarjetas.html',context_instance=RequestContext(request))

@login_required
def listado_descuentos_mes_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	filtro=request.GET.get('filtro')
	f1=request.GET.get('F1')
	m = f1.split('-')[1]
	y = f1.split('-')[0]
	f2=request.GET.get('F2')
	if request.is_ajax:
		try:
			consulta=list(TDetalleDescuento.objects.filter(ReporteDiario__Grifo=pkGrifo,ReporteDiario__FechaFinal__month=m,ReporteDiario__FechaFinal__year=y).values('pk','NroVale','Titular','ReporteDiario','Concepto','Monto'))
			lista=[]
			total = 0
			for obj in consulta:
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['pk']=obj['pk']
				dato['nroVale']=obj['NroVale']
				dato['reporte']=obj['ReporteDiario']
				dato['titular']=titular.Nombre
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['Monto']),2)
				total=total+dato['monto']
				lista.append(dato)
			lista.append({'totalDescuentos':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_descuentos_mes_cliente_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			#reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m)
			descuentos = list(TDetalleDescuento.objects.filter(ReporteDiario__Grifo=pkEstacion,ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m).values('Titular').annotate(Monto=Sum('Monto')).order_by('-Monto'))
			lista=[]
			total=0
			for obj in descuentos:
				#pago = TPagos.objects.filter(ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular=obj['Titular']).aggregate(Monto=Sum('MontoAmortizado'))
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['nombre']= titular.Nombre[:30]

				#m_pago=0
				#if pago['Monto'] != None:
				#	m_pago=float(pago['Monto'])
				dato['descuento'] = float(obj['Monto'])#-m_pago
				total= total+dato['descuento']
				lista.append(dato)
			lista.append({'totalDescuento':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Descuento_reporte_mes_view(request):
	return render_to_response('reporteDescuentos.html',context_instance=RequestContext(request))

#**************************** PAGOS ******************************
@login_required
def listado_pagos_mes_view(request):
	pkGrifo=request.GET.get('pkGrifo')
	filtro=request.GET.get('filtro')
	f1=request.GET.get('F1')
	m = f1.split('-')[1]
	y = f1.split('-')[0]
	f2=request.GET.get('F2')
	if request.is_ajax:
		try:
			consulta=list(TPagos.objects.filter(ReporteDiario__Grifo=pkGrifo,ReporteDiario__FechaFinal__month=m,ReporteDiario__FechaFinal__year=y).values('pk','Titular','ReporteDiario','Concepto','MontoAmortizado'))
			lista=[]
			total = 0
			for obj in consulta:
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['pk']=obj['pk']
				dato['reporte']=obj['ReporteDiario']
				dato['titular']=titular.Nombre
				dato['concepto']=obj['Concepto']
				dato['monto']=round(float(obj['MontoAmortizado']),2)
				total=total+dato['monto']
				lista.append(dato)
			lista.append({'totalPagos':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def reporte_Pagos_mes_cliente_ajax_view(request):
	pkEstacion=request.GET.get('pkEstacion')
	mes=request.GET.get('mes')
	if request.is_ajax:
		try:
			m = mes.split('-')[1]
			y = mes.split('-')[0]
			#reporte=TReporteDiario.objects.filter(FechaFinal__year=y,FechaFinal__month=m)
			pagos = list(TPagos.objects.filter(ReporteDiario__Grifo=pkEstacion,ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m).values('Titular').annotate(Monto=Sum('MontoAmortizado')).order_by('-Monto'))
			lista=[]
			total=0
			for obj in pagos:
				#pago = TPagos.objects.filter(ReporteDiario__FechaFinal__year=y,ReporteDiario__FechaFinal__month=m,Titular=obj['Titular']).aggregate(Monto=Sum('MontoAmortizado'))
				titular = TTitular.objects.get(pk=obj['Titular'])
				dato={}
				dato['nombre']= titular.Nombre[:30]

				#m_pago=0
				#if pago['Monto'] != None:
				#	m_pago=float(pago['Monto'])
				dato['pago'] = float(obj['Monto'])#-m_pago
				total= total+dato['pago']
				lista.append(dato)
			lista.append({'totalPago':round(total,2)})
			data= json.dumps(lista)
		except:
			data='fail'+ str(sys.exc_info()[1])
	else:
		data='fail'
	mimetype="application/json"
	return HttpResponse(data,mimetype)

@login_required
def listado_Pago_reporte_mes_view(request):
	return render_to_response('reportePagos.html',context_instance=RequestContext(request))