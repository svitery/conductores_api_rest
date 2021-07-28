from django.conf.urls import url
from django.urls import path
import datos.views as views

"""
urls de la aplicación
datos/pedidos para el POST de pedidos
datos/pedidos/<str:fecha> para consultar los pedidos para una fecha determinada
datos/pedidos/<str:fecha>/<int:id_conductor> para consultar los pedidos por fecha y por id de conductor
datos/conductores/<str:fecha>/<int:hora>/<str:ubicacion> para consultar el conductor más cercano a una
    ubicación en una fecha y hora determinada
"""
urlpatterns = [
    path('datos/pedidos',views.post_pedido),
    path('datos/pedidos/<str:fecha>',views.get_pedidos_dia),
    path('datos/pedidos/<str:fecha>/<int:id_conductor>',views.get_conductor_dia),
    path('datos/conductores/<str:fecha>/<int:hora>/<str:ubicacion>',views.get_conductor_cercano)
]
