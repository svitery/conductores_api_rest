import datetime
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Pedido,Conductor
from .serializers import serializar_pedidos_dia, serializer_pedidos_id

from rest_framework.decorators import api_view


"""
Se recibe un JSON con las llaves:
id: int, representa el id del conductor
lat_start: latitud de inicio del pedido
lat_end: latitud del destino del pedido
long_start: longitud de inicio del pedido
long_end: longitud del destino del pedido
fecha: fecha del pedido en formato yyyy/mm/dd
hora: hora del pedido, entero de 0 al 23

Si se pudo agregar el pedido se responde un JSON con la llave "message"
El valor de la llave es "Pedido agregado correctamente"
De lo contrario, la llave del JSON es 'error' y su valor es un str con el error ocurrido
Si se pudo agregar el pedido se envía un status 200 OK
Si hubo algún error se envía un status 400 BAD REQUEST
"""
@api_view(['POST'])
def post_pedido(request):

    #Convertir el request a JSon
    json_request=JSONParser().parse(request)
    try:
        #Extraer los campos del json
        ide=json_request['id']
        lat_start=json_request['lat_start']
        lat_end=json_request['lat_end']
        long_start=json_request['long_start']
        long_end=json_request['long_end'] 
        fecha=json_request['fecha']
        hora=json_request['hora']

        #Verificar si el pedido inicia y termina en el mismo punto
        if lat_start==lat_end and long_start==long_end:
            return JsonResponse({'error':'El pedido inicia y termina en el mismo lugar'},status=status.HTTP_400_BAD_REQUEST)


        #Verificar el rango de la hora
        if hora<0 or hora>23:
            return JsonResponse({'error':'La hora no está en el rango permitido'},status=status.HTTP_400_BAD_REQUEST)

        año,mes,dia=fecha.split('/')
        
        #Verificar el tamaño de los str de año, mes y dia
        if len(año)!=4:
            return JsonResponse({'error':'El año tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

        if len(mes)!=2:
            return JsonResponse({'error':'El mes tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

        if len(dia)!=2:
            return JsonResponse({'error':'El dia tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

        #Si el mes o el día están en rangos incorrectos, se lanza una excepcion
        datetime.datetime(int(año),int(mes),int(dia))

        #Encontrar el conductor y ver si está libre
        conductor=Conductor.objects.get(pk=ide)
        libre=conductor.esta_libre(fecha,hora)
        
        #Si está libre se agrega el pedido, de lo contrario, se envía un mensaje de error
        if libre:
            pedido=Pedido(fecha=fecha,hora=hora,lat_start=lat_start,lat_end=lat_end,long_start=long_start,long_end=long_end)
            pedido.save()
            conductor.pedidos.add(pedido)
            return JsonResponse({'message':'Pedido añadido correctamente'},status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error':'Conductor ocupado'},status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        

"""
Recibe una peticion GET con una fecha que se pasa por la URL
La fecha tiene el formato yyyy-mm-dd
retorna una lista en formato JSON con los pedidos de esa fecha ordenados por hora
"""
@api_view(['GET'])
def get_pedidos_dia(request,fecha):
    #cambia los caracteres '-' que llegan en la url por '/'
    fecha=fecha.replace('-','/')
    
    #se obtienen todos los conductores y pedidos filtrados por la fecha ordenados por hora
    conductores=Conductor.objects.filter(pedidos__fecha=fecha).order_by('pedidos__hora')
    pedidos_pk=conductores.values('pedidos')
    
    #se pasan los conductores con sus respectivos pedidos a una lista de diccionarios
    lista=serializar_pedidos_dia(conductores,pedidos_pk)
    
    #se retorna la lista en formato JSON
    return JsonResponse(lista,safe=False)


"""
Recibe una peticion GET con una fecha y un id de conductor que se reciben por la URL
La fecha tiene el formato yyyy-mm-dd
El id es un entero
retorna una lista en formato JSON con los pedidos correspondientes a la fecha y el conductor

Si hay un error, retorna un JSON son la llave "message" con el mensaje de error con status 400 BAD REQUEST
"""
@api_view(['GET'])
def get_conductor_dia(request,fecha,id_conductor):
    try:
        #cambia los caracteres '-' que llegan en la url por '/'
        dia=fecha.replace('-','/')

        #busca el conductor correspondiente al id que llega por parámetro
        conductor=Conductor.objects.get(pk=id_conductor)
        
        #filtra los pedidos del conductor deseado por fecha
        pedidos=conductor.pedidos.all().filter(fecha=dia)
        
        #los pedidos encontrados se pasan a una lista de diccionarios
        lista=serializer_pedidos_id(pedidos)
        
        #Se retorna la lista de diccionarios en formato JSON
        return JsonResponse(lista,safe=False)
    except Exception as e:
        #se retorna un bad request con el mensaje de error
        return JsonResponse({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    

"""
Recibe una petición GET con una fecha, hora y id de conductor que se re
Busca el conductor más cercano a una ubicacion en una fecha y hora
La fecha tiene el formato yyyy-mm-dd
La hora es un entero del 0 al 23
La ubicación es tiene el formato latitud,longitud

Se retorna un JSON con las llaves:
'id' que corresponde al id del conductor más cercano
'lat' que corresponde a la latitud del conductor más cercano
'long' que corresponde a la longitud del conductor más cercano
Si no hubo errores se retorna un status 200 OK

Si hubo algún error se retorna un JSON con la llave 'error' que contiene el mensaje de la excepción
junto con un status 400 BAD REQUEST
"""
@api_view(['GET'])
def get_conductor_cercano(request,fecha,hora,ubicacion):
    try:
        #Cambiar los caracteres '-' de la fecha por '/'
        fecha=fecha.replace('-','/')

        #Se hace una petición de todos los conductores
        conductores=Conductor.objects.all()
        
        #Separar latitud y longitud a partir de los datos que llegan por parámetro
        ubicacion=ubicacion.split(',')
        lat_req=float(ubicacion[0])
        long_req=float(ubicacion[1])
        
        #Inicializar el conductor más cercano y la distancia más cercana para hacer el algoritmo del menor
        conductor_cercano=conductores[0]
        distancia_menor=float('inf')
        
        #Recorrer todos los conductores buscando el que está más cerca
        for conductor in conductores:
            ubicacion_actual=conductor.ubicacion_hora(fecha,hora)
            distancia=(ubicacion_actual[0]-lat_req)**2+(ubicacion_actual[1]-long_req)**2
            if distancia<distancia_menor:
                distancia_menor=distancia
                conductor_cercano=conductor
                lat_conductor,long_conductor=ubicacion_actual
        
        #Se hace un diccionario con las llaves 'id', 'lat' y 'long' y se lo retorna como un JSON
        dicc_resp={'id':conductor_cercano.id,'lat':lat_conductor,'long':long_conductor}
        return JsonResponse(dicc_resp,status=status.HTTP_200_OK)

    except Exception as e: 
        #Se retorna un status 400 junto con un JSON que contiene el mensaje de error
        return JsonResponse({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
