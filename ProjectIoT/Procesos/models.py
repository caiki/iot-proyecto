# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.


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