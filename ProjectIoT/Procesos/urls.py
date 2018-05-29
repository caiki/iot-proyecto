from django.conf.urls import patterns, url
urlpatterns= patterns('Procesos.views', 
					  url(r'^heart/', 'Depositos_view')
					 )
