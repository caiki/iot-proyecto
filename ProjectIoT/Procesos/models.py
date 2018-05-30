# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class TTitular(models.Model):
    """docsrting for Cliente"""
    idTitular = models.AutoField("Id", primary_key=True)
    Nombre = models.CharField("Nombre:", max_length=100,blank= True, null=True)
    DocID = models.CharField("Teléfono:", max_length=15,blank= True, null=True)
    Debito=models.DecimalField(max_digits=15,decimal_places=3)
    Credito=models.DecimalField(max_digits=15,decimal_places=3)
    class Meta:
        ordering = ["idTitular"]
        verbose_name_plural = "Titulares"
        verbose_name = "Titular"

    def __str__(self):
        return str(self.idTitular)

class Grifo(models.Model):
    """docsrting for Cliente"""
    idGrifo = models.AutoField("Id", primary_key=True)
    NombreEstacion = models.CharField("NombreEstacion:", max_length=50,blank= True, null=True)
    Administrador = models.CharField("Administrador:", max_length=50,blank= True, null=True)
    
    class Meta:
        ordering = ["idGrifo"]
        verbose_name_plural = "Grifos"
        verbose_name = "Grifo"

    def __str__(self):
        return str(self.idGrifo)

#------------------------------------------------------------------
class Surtidor(models.Model):
    """docsrting for Cliente"""
    idSurtidor = models.AutoField("Id", primary_key=True)
    NombreSurtidor = models.CharField("NombreSurtidor:", max_length=50,blank= True, null=True)
    Grifo=models.ForeignKey(Grifo,verbose_name='Id Grifo')
    
    class Meta:
        ordering = ["idSurtidor"]
        verbose_name_plural = "Surtidores"
        verbose_name = "Surtidor"

    def __str__(self):
        return str(self.idSurtidor)

class TCombustible(models.Model):
    """docsrting for Cliente"""
    idCombustible = models.AutoField("Id", primary_key=True)
    NombreCombustible = models.CharField("NombreCombustible:", max_length=20,blank= True, null=True)
    
    class Meta:
        ordering = ["idCombustible"]
        verbose_name_plural = "TCombustibles"
        verbose_name = "TCombustible"

    def __str__(self):
        return str(self.idCombustible)

class TManguera(models.Model):
    """docsrting for Cliente"""
    idManguera = models.AutoField("Id", primary_key=True)
    NombreManguera = models.CharField("NombreManguera:", max_length=6,blank= True, null=True)
    Combustible=models.ForeignKey(TCombustible,verbose_name='Id Combustible')
    Surtidor=models.ForeignKey(Surtidor,verbose_name='Id Surtidor')
#<<<<<<< HEAD
#=======
    Tanque = models.CharField("Tanque:", max_length=15,blank= True, null=True)#defaul "n"
#>>>>>>> 371d9c22e7544096615209f22653858214f756b9
    
    class Meta:
        ordering = ["idManguera"]
        verbose_name_plural = "Mangueras"
        verbose_name = "Manguera"

    def __str__(self):
        return str(self.idManguera)

class Tanque(models.Model):
    """docsrting for Cliente"""
    idTanque = models.AutoField("Id", primary_key=True)
    Nombre = models.CharField("Nombre:", max_length=15,blank= True, null=True)
    Combustible=models.ForeignKey(TCombustible,verbose_name='Id Combustible')
    Grifo=models.ForeignKey(Grifo,verbose_name='Id Grifo')
    
    class Meta:
        ordering = ["idTanque"]
        verbose_name_plural = "Tanques"
        verbose_name = "Tanque"

    def __str__(self):
        return str(self.idTanque)
#------------------------------------------------------------------
class TReporteDiario(models.Model):
    """docsrting for Caja Debe"""
    idReporteDiario = models.AutoField("ID:", primary_key=True)
    #NombreEstacion=models.CharField("Estacion:",max_length=50)
    Fecha = models.DateTimeField("Fecha:",auto_now=True)
    FechaInicial = models.DateField("Fecha inicial:")
    FechaFinal = models.DateField("Fecha final:")
    Griferos=models.CharField("Griferos:",max_length=250)
    Grifo=models.ForeignKey(Grifo,verbose_name='Id Grifo')
    DepositoBancos=models.DecimalField(max_digits=15,decimal_places=3)#efectivo entregado por los griferos
    SaldoCredito=models.DecimalField(max_digits=15,decimal_places=3)
    SaldoGastos=models.DecimalField(max_digits=15,decimal_places=3)
    Observacion = models.CharField("Observacion:", max_length=300,blank= True, null=True)
    #Administrador=models.CharField("Administrador:",max_length=50)

    class Meta:
        ordering = ["idReporteDiario"]
        verbose_name_plural = "Reportes Diarios"
        verbose_name = "Reporte Diario"

    def __str__(self):
        return str(self.idReporteDiario)

class PrecioCombustible(models.Model):#forenkey a manguera
    """docsrting for Cliente"""
    idPrecioComb = models.AutoField("Id", primary_key=True)
    Fecha = models.DateTimeField("Fecha:",auto_now=True)
    Combustible=models.ForeignKey(TCombustible,verbose_name='Id Combustible')
    Grifo=models.ForeignKey(Grifo,verbose_name='Id Grifo')
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    PrecioAnterior=models.DecimalField(max_digits=15,decimal_places=3,default=0)
    PrecioActual=models.DecimalField(max_digits=15,decimal_places=3)
    class Meta:
        ordering = ["idPrecioComb"]
        verbose_name_plural = "Precios Combustible"
        verbose_name = "Precio Combustible"
        
    def __str__(self):
        return str(self.idPrecioComb)

class LecturaContometro(models.Model):
    """docsrting for Cliente"""
    idLectura = models.AutoField("Id", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    Manguera=models.ForeignKey(TManguera,verbose_name='Id Manguera')
    ValorContometroFinal1=models.DecimalField(max_digits=15,decimal_places=3)#Final Dia
    ValorContometroFinal2=models.DecimalField(max_digits=15,decimal_places=3)#Final Noche

    class Meta:
        ordering = ["idLectura"]
        verbose_name_plural = "Lecturas de Contometro"
        verbose_name = "Lectura de Contometro"

    def __str__(self):
        return str(self.idLectura)

class TDetalleCreditos(models.Model):
    """docsrting for Caja Debe"""
    idDetalleCredito = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    NroVale = models.CharField("Concepto:", max_length=10,blank= True, null=True)
    Titular=models.ForeignKey(TTitular,verbose_name='Id Titular')
    Concepto = models.CharField("Concepto:", max_length=100,blank= True, null=True)
    Monto=models.DecimalField(max_digits=15,decimal_places=2)

    class Meta:
        ordering = ["idDetalleCredito"]
        verbose_name_plural = "Detalles Credito"
        verbose_name = "Detalle Credito"

    def __str__(self):
        return str(self.idDetalleCredito)

class TDetalleDescuento(models.Model):
    """docsrting for Descuento"""
    idDetalleDescuento = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    NroVale = models.CharField("Concepto:", max_length=10,blank= True, null=True)
    Titular=models.ForeignKey(TTitular,verbose_name='Id Titular')
    Concepto = models.CharField("Concepto:", max_length=100,blank= True, null=True)
    Monto=models.DecimalField(max_digits=15,decimal_places=2)

    class Meta:
        ordering = ["idDetalleDescuento"]
        verbose_name_plural = "Detalles Descuento"
        verbose_name = "Detalle Descuento"

    def __str__(self):
        return str(self.idDetalleDescuento)

class Tdeposito(models.Model):
    """docsrting for Caja Debe"""
    idDeposito = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    NroBoucher = models.CharField("NroBoucher:", max_length=45,blank= True, null=True)
    Concepto = models.CharField("Concepto:", max_length=100,blank= True, null=True)
    Monto=models.DecimalField(max_digits=15,decimal_places=2)

    class Meta:
        ordering = ["idDeposito"]
        verbose_name_plural = "Depositos"
        verbose_name = "Deposito"

    def __str__(self):
        return str(self.idDeposito)

class TPagos(models.Model):
    """docsrting for Caja Debe"""
    idPago = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    Concepto = models.CharField("Concepto:", max_length=100,blank= True, null=True)
    MontoAmortizado=models.DecimalField(max_digits=15,decimal_places=2)
    Titular=models.ForeignKey(TTitular,verbose_name='Id Titular')
    class Meta:
        ordering = ["idPago"]
        verbose_name_plural = "Pagos"
        verbose_name = "Pago"

    def __str__(self):
        return str(self.idPago)

class TDetalleGastos(models.Model):
    """docsrting for Caja Debe"""
    idDetalleGasto = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    NroVale = models.CharField("Nro Vale:",max_length=10,blank= True, null=True)
    #Titular = models.CharField("Titular:", max_length=100,blank= True, null=True)
    Concepto = models.CharField("Concepto:", max_length=100,blank= True, null=True)
    Monto=models.DecimalField(max_digits=15,decimal_places=2)
    class Meta:
        ordering = ["idDetalleGasto"]
        verbose_name_plural = "Detalles Gastos"
        verbose_name = "Detalle Gasto"

    def __str__(self):
        return str(self.idDetalleGasto)

#------------------------------------------------------------------
class TDetalleSerafin(models.Model):
    """docsrting for Caja Debe"""
    idDetalleSerafin = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    NroVale = models.CharField("Nro Vale:",max_length=10,blank= True, null=True)
    Cantidad =models.DecimalField (max_digits=15,decimal_places=2)
    Combustible=models.ForeignKey(TCombustible,verbose_name='Id Combustible')
    Observacion = models.CharField("Observacion:", max_length=100,blank= True, null=True)
    Monto=models.DecimalField(max_digits=15,decimal_places=2)
    class Meta:
        ordering = ["idDetalleSerafin"]
        verbose_name_plural = "Detalles Serafin"
        verbose_name = "Detalle Serafin"

    def __str__(self):
        return str(self.idDetalleGasto)

#----------------------------------------------
class TMovimientoVista(models.Model):
    """docsrting for Caja Debe"""
    idMovimientoVista = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    Tanque=models.ForeignKey(Tanque,verbose_name='Tanque')
    IngresoTransferencia=models.DecimalField(max_digits=15,decimal_places=3)
    IngresoTransferenciaContable=models.DecimalField(max_digits=15,decimal_places=3)
    #SaldoActual=models.DecimalField(max_digits=15,decimal_places=3)
    #SaldoActualMovContable=models.DecimalField(max_digits=15,decimal_places=3,default=0)
    #SaldoAcumulado=models.DecimalField(max_digits=15,decimal_places=3)
    Motivo = models.CharField("Motivo:", max_length=100,blank= True, null=True)
    Titular=models.ForeignKey(TTitular,verbose_name='Id Titular', null=True)
    Observacion = models.CharField("Observacion:", max_length=100,blank= True, null=True)
    #Punitario=models.DecimalField(max_digits=15,decimal_places=2,default=0)
    class Meta:
        ordering = ["idMovimientoVista"]
        verbose_name_plural = "Movimientos Vista"
        verbose_name = "Movimiento Vista"

    def __str__(self):
        return str(self.idMovimientoVista)

#----------------------------------------------
class TSaldoCombustible(models.Model):
    """Lectura de Combustible disponible"""
    idSaldoCombustible = models.AutoField("ID:", primary_key=True)
    ReporteDiario=models.ForeignKey(TReporteDiario,verbose_name='Id Reporte')
    Tanque=models.ForeignKey(Tanque,verbose_name='Tanque')
    SaldoActual=models.DecimalField(max_digits=15,decimal_places=3)
    SaldoActualMovContable=models.DecimalField(max_digits=15,decimal_places=3,default=0)
    class Meta:
        ordering = ["idSaldoCombustible"]
        verbose_name_plural = "Saldos Combustible"
        verbose_name = "Saldo Combustible"

    def __str__(self):
        return str(self.idSaldoCombustible)

#----------------------------------------------

class TCompra(models.Model):
    """docsrting for Caja Debe"""
    idCompra = models.AutoField("ID:", primary_key=True)
    FechaCompra = models.DateField("Fecha compra:")
    NroDocumento = models.CharField("Concepto:", max_length=10,blank= True, null=True)
    #Titular=models.ForeignKey(TTitular,verbose_name='Id Titular', null=True)
    #Tanque=models.ForeignKey(Tanque,verbose_name='Tanque')
    idMovimientoVista = models.ForeignKey(TMovimientoVista, verbose_name='Movimiento Vista',null=True)
    Punitario=models.DecimalField(max_digits=15,decimal_places=2,default=0) #ValorUnitarioCompra
    NotaCredito = models.CharField("NotaCredito:", max_length=20,blank= True, null=True)
    TransporteGalon = models.DecimalField(max_digits=15,decimal_places=2,default=0) #PrecioUnitarioTransporteGalon
    Observacion = models.CharField("Observacion", max_length=250,blank= True, null=True)
    Igv = models.DecimalField("IGV",max_digits=15,decimal_places=2,default=18)
    Percepcion = models.DecimalField("Percepcion",max_digits=15,decimal_places=2,default=1)
    FechaPago = models.DateField("Fecha Pago:")
    NroCheque = models.CharField("NroCheque:", max_length=20,blank= True, null=True)

    class Meta:
        ordering = ["idCompra"]
        verbose_name_plural = "COMPRAS"
        verbose_name = "COMPRA"

    def __str__(self):
        return str(self.idCompra)

#----------------config inicio -------------------------------------

class Inicio(models.Model):
    """docsrting for Cliente"""
    idInicio = models.AutoField("Id", primary_key=True)
    Grifo=models.ForeignKey(Grifo,verbose_name='Id Grifo')#id grifo
    aux1 = models.CharField("aux1:", max_length=20,blank= True, null=True)
    aux2 = models.CharField("aux2:", max_length=20,blank= True, null=True)
    class Meta:
        ordering = ["idInicio"]
        verbose_name_plural = "Inicios"
        verbose_name = "Inicio"

    def __str__(self):
        return str(self.idInicio)

#----------------------------------------------

class THeart(models.Model):
    """docsrting for Caja Debe"""
    idHeart = models.AutoField("ID:", primary_key=True)
    FechaTiempo = models.DateTimeField("FechaTiempo:")
    Beat = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    
    class Meta:
        ordering = ["idHeart"]
        verbose_name_plural = "Hearts"
        verbose_name = "Heart"

    def __str__(self):
        return str(self.idHeart)
'''
class TPagoProveedor(models.Model):
    idPagoProveedor 

'''