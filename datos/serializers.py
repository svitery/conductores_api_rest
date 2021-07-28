from .models import Pedido

"""
Recibe QuerySets de conductores y pedidos y retorna una lista de diccionarios con las siguientes llaves:
    'id': entero con el id del conductor
    'hora': entero que representa la hora del pedido
    'lat_start': float que representa la latitud de inicio del pedido
    'lat_end': float que representa la latitud de destino del pedido
    'long_start': float que representa la longitud de inicio del pedido
    'long_end': float que representa la longitud de destino del pedido
"""
def serializar_pedidos_dia(conductores,pedidos):
    #Se inicializa la lista que se va a retornar como una lista vacía
    lista=[]

    #Se recorren los pedidos y conductores(los dos tienen el mismo tamaño)
    for i in range(len(pedidos)):
        #Se obtiene el id del conductor y la llave primaria del pedido
        id_conductor=conductores[i].id
        id_pedido=pedidos[i]['pedidos']

        #Se obtiene el pedido correspondiente a la llave primaria
        pedido=Pedido.objects.get(pk=id_pedido)
        
        #Se genera el diccionario con el formato deseado
        dicc={
            'id':id_conductor,
            'hora':pedido.hora,
            'lat_start':pedido.lat_start,
            'lat_end':pedido.lat_end,
            'long_start':pedido.long_start,
            'long_end':pedido.long_end
            }
        
        #Se agrega el diccionario a la lista que se va a retornar
        lista.append(dicc)
    
    #Se retorna la lista de diccionarios
    return lista

"""
Recibe un QuerySet de pedidos y retorna una lista de diccionarios con las siguientes llaves
    'hora': entero que representa la hora del pedido
    'lat_start': float que representa la latitud de inicio del pedido 
    'lat_end': float que representa la latitud de destino del pedido 
    'long_start': float que representa la longitud de inicio del pedido 
    'long_end': float que representa la longitud de destino del pedido    

"""
def serializer_pedidos_id(pedidos):
    #Se inicializa la lista que se va a retornar como una lista vacía
    lista=[]

    #Se recorren los pedidos
    for pedido in pedidos:

        #Se genera el diccionario con el formato deseado
        dicc={
            'hora':pedido.hora,
            'lat_start':pedido.lat_start,
            'lat_end':pedido.lat_end,
            'long_start':pedido.long_start,
            'long_end':pedido.long_end
        }

        #Se agrega el diccionario a la lista que se va a retornar
        lista.append(dicc)
    
    #Se retorna la lista de diccionarios
    return lista
