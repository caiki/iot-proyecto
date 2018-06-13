from django.contrib import admin
from .models import *
# Register your models here.

"""class DepositoAdmin(admin.ModelAdmin):
	list_display = ('idDeposito','ReporteDiario','NroBoucher','Concepto','Monto')
	pass
admin.site.register(Tdeposito,DepositoAdmin)
"""

class Heart(admin.ModelAdmin):
	list_display = ('idHeart','FechaTiempo','Beat')
	pass
admin.site.register(THeart,Heart)