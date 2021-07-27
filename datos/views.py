import datetime
from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework import status

from .models import Pedido,Conductor
from .serializers import serializar_pedidos_dia, serializer_pedidos_id

from rest_framework.decorators import api_view


"""
Se recibe un JSON con las llaves id, lat_start, lat_end, long_start, long_end,fecha,hora
fecha tiene el formato año/mes/dia
hora es un entero del 0 al 23
"""
@api_view(['POST'])
def post_pedido(request):
    if request.method=='POST':
        json_request=JSONParser().parse(request)
        try:
            ide=json_request['id']
            lat_start=json_request['lat_start']
            lat_end=json_request['lat_end']
            long_start=json_request['long_start']
            long_end=json_request['long_end'] 
            fecha=json_request['fecha']
            hora=json_request['hora']

            """
                Falta verificar que los pedidos no inicien y terminen en el mismo lugars
            """

            #Verificar formato de fecha y hora
            if hora<0 or hora>23:
                return JsonResponse({'message':'La hora no está en el rango permitido'},status=status.HTTP_400_BAD_REQUEST)

            año,mes,dia=fecha.split('/')

            if len(año)!=4:
                return JsonResponse({'message':'El año tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

            if len(mes)!=2:
                return JsonResponse({'message':'El mes tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

            if len(mes)!=2:
                return JsonResponse({'message':'El mes tiene un formato incorrecto'},status=status.HTTP_400_BAD_REQUEST)

            #Si el mes o el día están en rangos incorrectos, se lanza una excepcion
            fecha_datetime=datetime.datetime(int(año),int(mes),int(dia))

            conductor=Conductor.objects.get(pk=ide)
            libre=conductor.esta_libre(fecha,hora)
            if libre:
                pedido=Pedido(fecha=fecha,hora=hora,lat_start=lat_start,lat_end=lat_end,long_start=long_start,long_end=long_end)
                pedido.save()
                conductor.pedidos.add(pedido)
                return JsonResponse({'message':'Pedido añadido correctamente'},status=status.HTTP_200_OK)
            else:
                return JsonResponse({'message':'Conductor ocupado'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            #print(e)
            return JsonResponse({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
def get_pedidos_dia(request,dia):
    fecha=dia.replace('-','/')
    conductores=Conductor.objects.filter(pedidos__fecha=fecha).order_by('pedidos__hora')
    pedidos_pk=conductores.values('pedidos')
    lista=serializar_pedidos_dia(conductores,pedidos_pk)
    return JsonResponse(lista,safe=False)


@api_view(['GET'])
def get_conductor_dia(request,dia,id_conductor):
    try:
        dia=dia.replace('-','/')
        conductor=Conductor.objects.get(pk=id_conductor)
        pedidos=conductor.pedidos.all().filter(fecha=dia)
        lista=serializer_pedidos_id(pedidos)
        return JsonResponse(lista,safe=False)
    except Exception as e:
        return JsonResponse({'h':str(e)})
    

@api_view(['GET'])
def get_conductor_cercano(request,dia,hora,ubicacion):
    try:
        fecha=dia.replace('-','/')
        conductores=Conductor.objects.all()
        ubicacion=ubicacion.split(',')
        print(fecha,hora)
        lat_req=float(ubicacion[0])
        long_req=float(ubicacion[1])
        
        conductor_cercano=conductores[0]
        distancia_menor=float('inf')
        
        for conductor in conductores:
            ubicacion_actual=conductor.ubicacion_hora(fecha,hora)
            distancia=(ubicacion_actual[0]-lat_req)**2+(ubicacion_actual[1]-long_req)**2
            if distancia<distancia_menor:
                distancia_menor=distancia
                conductor_cercano=conductor
                lat_conductor,long_conductor=ubicacion_actual
        dicc_resp={'id':conductor_cercano.id,'lat':lat_conductor,'long':long_conductor}
        return JsonResponse(dicc_resp,status=status.HTTP_200_OK)

    except Exception as e: 
        print(str(e))
        return JsonResponse({'error':str(e)})
