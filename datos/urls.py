from django.conf.urls import url
from django.urls import path
import datos.views as views

urlpatterns = [
    path('datos/pedidos',views.post_pedido),
    path('datos/pedidos/<str:dia>',views.get_pedidos_dia),
    path('datos/pedidos/<str:dia>/<int:id_conductor>',views.get_conductor_dia),
    path('datos/conductor_cercano/<str:dia>/<int:hora>/<str:ubicacion>',views.get_conductor_cercano)
]
