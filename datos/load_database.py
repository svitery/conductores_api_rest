import requests
import time
from threading import Thread
from .models import Conductor

"""
Lee un archivo de un endpoint y lo retorna en formato JSON
"""
def cargar_json(ruta='https://gist.githubusercontent.com/CesarF/41958f4bc34240b75a83fce876836044/raw/b524588cb979fc6e3ec5a8913ee497d64509e888/locations.json'):
    file=requests.get(ruta)
    return file.json()


"""
Carga los conductores a la base de datos a partir de un archivo JSON
"""
def json_to_database(json_file):
    for item in json_file:
        id=item['id']
        lat=item['lat']
        long=item['long']

        #Lee el item last_update y lo separa en dia, mes y año como enteros
        mes,dia,año=tuple(map(int,item['last_update'].split('/')))
        
        #Pone el mes y el día como cadenas de dos caracteres
        if mes <10:
            mes='0'+str(mes)
        if dia<10:
            dia='0'+str(dia)
        
        #Genera una entrada de la base de datos
        entry=Conductor(id=id,lat=lat,long=long,last_update=f'{año}/{mes}/{dia}')
        entry.save()
        
"""
Actualiza la base de datos periódicamente con la información del endpoint
"""
def update_database(ruta='https://gist.githubusercontent.com/CesarF/41958f4bc34240b75a83fce876836044/raw/b524588cb979fc6e3ec5a8913ee497d64509e888/locations.json',wait_time=10,errores=0):
    try:
        #Repite el proceso constantemente mientras no se haya alcanzado el límite de errores
        while True and errores<10:
            json_file=cargar_json(ruta=ruta)
            
            #Itera sobre los elementos del JSON y actualiza la base de datos
            for item in json_file:
                id=item['id']
                lat=item['lat']
                long=item['long']
                mes,dia,año=tuple(map(int,item['last_update'].split('/')))
                if mes <10:
                    mes='0'+str(mes)
                if dia<10:
                    dia='0'+str(dia)
                
                #Busca el conductor, si se lanza una excepción significa que el elemento no existe
                #y debe crearlo, de lo contrario actualiza los campos
                try:
                    entry=Conductor.objects.get(pk=id)
                    c=entry
                    c.lat=lat
                    c.long=long
                    c.last_update=f'{año}/{mes}/{dia}'
                except:
                    c=Conductor(id=id,lat=lat,long=long,last_update=f'{año}/{mes}/{dia}')
                c.save()

            #Espera un tiempo para volver a consultar
            time.sleep(wait_time)
        
        #Si sale del ciclo significa que se alcanzó el límite de errores en la conexión
        print('se perdió la conexión con el endpoint')
    
    #Si hubo un error lo imprime y vuelve a llamar la función aumentando en 1 el número de errores
    except Exception as e:
        print(str(e))
        time.sleep(wait_time)
        update_database(errores=errores+1)

#Carga el JSON y genera las entradas de la base de datos
json=cargar_json()
json_to_database(json)

#Crea el hilo que se va a encargar de actualizar la base de datos a partir del endpoint
thread=Thread(target=update_database)
thread.start()