from django.db import models

# Create your models here.

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

    def esta_libre(self,fecha,hora):
        print(fecha)
        pedidos_q=self.pedidos.filter(fecha=fecha).filter(hora=hora)
        if len(pedidos_q)==0:
            return True
        else:
            return False


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
            
    def __hora_cercana(self,horas,hora):
        for hora_it in horas:
            if hora_it==hora or hora_it<hora:
                return hora_it

    def ubicacion_hora(self,fecha,hora):
        c_pedidos=self.pedidos.order_by('fecha')
        fechas=c_pedidos.values_list('fecha',flat=True).distinct()
        #print('fechas',fechas)
        #Si no tiene pedidos
        if len(c_pedidos)==0:
            return (self.lat,self.long)
        else:
            #print('aqui')
            fecha_cercana=self.__fecha_cercana(fecha,fechas[::-1])
            pedidos_fecha=c_pedidos.filter(fecha=fecha_cercana).order_by('hora')
            if len(pedidos_fecha)==0:#significa que la fecha es last update
                return (self.lat,self.long)
            else:#Encontrar la hora
                
                horas=pedidos_fecha.values_list('hora',flat=True)[::-1]
                hora_pedido=self.__hora_cercana(horas,hora)

                if hora_pedido==None:#regresar al pedido anterior
                    index=fechas[::-1].index(fecha_cercana)
                    if index==0:
                        return (self.lat,self.long)
                    else:
                        fecha_cercana=fechas[index-1]
                        #Ahora buscar el ultimo pedido de la última fecha cercana
                        pedidos_fecha=c_pedidos.filter(fecha=fecha_cercana).order_by('hora')
                        ultimo_pedido=pedidos_fecha[-1]
                        return (ultimo_pedido.lat_end,ultimo_pedido.long_end)

                pedido=pedidos_fecha.filter(hora=hora_pedido)
                pedido=pedido[0]
                if hora_pedido==hora:
                    return (pedido.lat_start,pedido.long_start)
                else:
                    return (pedido.lat_end,pedido.long_end)


