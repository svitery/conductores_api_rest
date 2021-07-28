from django.db import models

"""
Representa un pedido con los campos:
fecha: cadena de caracteres que representa la fecha del pedido en el formato yyyy/mm/dd
hora: entero que representa la hora del pedido - es un entero del 0 al 23
lat_start: float que representa la latitud de inicio del pedido
lat_end: float que representa la latitud de destino del pedido
long_start: float que representa la longitud de inicio del pedido
long_end: float que representa la longitud de destino del pedido
"""
class Pedido(models.Model):
    fecha=models.CharField(max_length=10,default='0000/00/00')
    hora=models.IntegerField(default=0)
    lat_start=models.FloatField()
    lat_end=models.FloatField()
    long_start=models.FloatField()
    long_end=models.FloatField()

    class Meta:
        ordering=['fecha','hora']

    def __str__(self):
        return f'{self.fecha}-{self.hora}'

    
"""
Representa un conductor con los campos:
id: entero que representa el id del conductor
last_update: cadena de caracteres que representa la fecha de la última actualización obtenida a través
    del endpoint. Tiene el formato yyyy/mm/dd
lat: float que representa la latitud del conductor obtenida a través del endpoint
long: float que representa la longitud del conductor obtenida a través del endpoint

pedidos: relaciones a los pedidos
"""
class Conductor(models.Model):
    id=models.IntegerField(primary_key=True)
    last_update=models.CharField(max_length=10)
    lat=models.FloatField()
    long=models.FloatField()
    pedidos=models.ManyToManyField(Pedido,blank=True)

    class Meta:
        ordering=['id']

    def __str__(self):
        return str(self.id)

    """
    Método que retorna True si un conductor está disponible en una fecha y hora determinadas,
    retorna False si ya tiene un pedido agendado
    """
    def esta_libre(self,fecha,hora):
        print(fecha)
        pedidos_q=self.pedidos.filter(fecha=fecha).filter(hora=hora)
        if len(pedidos_q)==0:
            return True
        else:
            return False

    """
    Retorna la fecha anterior más cercana a una fecha que llega por parámetro, buscando en una
    lista de fechas que llega como parámetro
    Por defecto, retorna la fecha correspondiente a last_update 
    La lista de fechas que llega por parámetro está ordenada de forma descendiente
    """
    def __fecha_cercana(self,fecha,fechas):
        
        if self.last_update==fecha:
            return self.last_update
        else:
            encontro=False
            for fecha_it in fechas:
                if fecha_it==fecha:
                    return fecha_it
                elif fecha_it<fecha:
                    fecha_pedido=fecha_it
                    encontro=True
                    break
            if encontro:
                if self.last_update<fecha and self.last_update>fecha_pedido:
                    return self.last_update
                else:
                    return fecha_pedido
        return self.last_update
            

    """
    Retorna la hora anterior más cercana a una hora que llega por parámetro, buscando en una 
    lista de horas que llega como parámetro
    Por defecto, retorna None
    La lista de horas que llega por parámetro está ordenada de forma
    """
    def __hora_cercana(self,horas,hora):
        for hora_it in horas:
            if hora_it==hora or hora_it<hora:
                return hora_it


    """
    Retorna la ubicación de un conductor a una fecha y hora determinada con una tupla de la 
        forma (latitud,longitud)
    Se asume que el conductor permanece en la ubicación donde finaliza el último pedido hasta que se
        agende un pedido nuevo
    """
    def ubicacion_hora(self,fecha,hora):
        #Se obtienen los pedidos ordenados por fecha
        c_pedidos=self.pedidos.order_by('fecha')

        #Se obtiene una lista de fechas en las que el conductor tiene pedidos (cada fecha aparece)
        #solo una vez
        fechas=c_pedidos.values_list('fecha',flat=True).distinct()

        #Si no tiene pedidos se retorna la fecha que se obtuvo del endpoint
        if len(c_pedidos)==0:
            return (self.lat,self.long)
        else:
            
            #Se obtiene la fecha más cercana a la fecha objetivo a partir de las fechas en las que 
            #el conductor tiene pedidos
            fecha_cercana=self.__fecha_cercana(fecha,fechas[::-1])

            #Se consultan los pedidos de la fecha más cercana
            pedidos_fecha=c_pedidos.filter(fecha=fecha_cercana).order_by('hora')
            
            #Si no hay pedidos en esa fecha se retorna la fecha obtenido a del endpoint
            if len(pedidos_fecha)==0:
                return (self.lat,self.long)
            
            #Si tiene pedidos, se pasa a buscar la hora más cercana
            else:
                
                #Se obtiene la lista de horas en las que el conductor tiene pedidos en la fecha
                #encontrada
                horas=pedidos_fecha.values_list('hora',flat=True)[::-1]
                
                #Se encuentra la hora anterior más cercana a la hora que llega por parámetro
                hora_pedido=self.__hora_cercana(horas,hora)

                #Si la hora encontrada es None, significa que todas las horas de pedidos en la fecha
                #son mayores a la hora que llega por parámetro y se debe retroceder la fecha
                if hora_pedido==None:

                    #Se obtiene el índice de la fecha 
                    index=fechas[::-1].index(fecha_cercana)
                    
                    #Si el índice de la fecha es 0, significa que no hay fechas anteriores, y por lo 
                    #tanto se retorna los valores obtenidos a través del endpoint
                    if index==0:
                        return (self.lat,self.long)
                    
                    #Si el índice de la fecha es 1, significa que hay pedidos anteriores
                    else:
                        #Se obtiene la fecha anterior
                        fecha_cercana=fechas[index-1]
                        
                        #Se obtiene el último pedido de la fecha anterior y se retorna la ubicación
                        #de destino
                        pedidos_fecha=c_pedidos.filter(fecha=fecha_cercana).order_by('hora')
                        ultimo_pedido=pedidos_fecha[-1]
                        return (ultimo_pedido.lat_end,ultimo_pedido.long_end)
                
                #Si la hora encontrada es diferente de None
                else:
                    #Se obtiene el pedido correspondiente a la hora más cercana
                    pedido=pedidos_fecha.filter(hora=hora_pedido)
                    pedido=pedido[0]

                    #Si la hora más cercana es igual a la que llega por parámetro, se retorna la 
                    #ubicación de inicio del pedido
                    if hora_pedido==hora:
                        return (pedido.lat_start,pedido.long_start)
                    
                    #De lo contrario se retorna la ubicación destino del pedido
                    else:
                        return (pedido.lat_end,pedido.long_end)


