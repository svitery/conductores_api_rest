from .models import Pedido

def serializar_pedidos_dia(conductores,pedidos):
    lista=[]
    for i in range(len(pedidos)):
        id_conductor=conductores[i].id
        id_pedido=pedidos[i]['pedidos']
        pedido=Pedido.objects.get(pk=id_pedido)
        dicc={
            'id':id_conductor,
            'hora':pedido.hora,
            'lat_start':pedido.lat_start,
            'lat_end':pedido.lat_end,
            'long_start':pedido.long_start,
            'long_end':pedido.long_end
            }
        lista.append(dicc)
    return lista


def serializer_pedidos_id(pedidos):
    lista=[]
    for pedido in pedidos:
        dicc={
            'hora':pedido.hora,
            'lat_start':pedido.lat_start,
            'lat_end':pedido.lat_end,
            'long_start':pedido.long_start,
            'long_end':pedido.long_end
        }
        lista.append(dicc)
    return lista
