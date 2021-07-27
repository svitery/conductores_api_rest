import requests
import time
from threading import Thread
from .models import Conductor

def cargar_json(ruta='https://gist.githubusercontent.com/CesarF/41958f4bc34240b75a83fce876836044/raw/b524588cb979fc6e3ec5a8913ee497d64509e888/locations.json'):
    file=requests.get(ruta)
    return file.json()


def json_to_database(json_file):
    for item in json_file:
        id=item['id']
        lat=item['lat']
        long=item['long']
        mes,dia,año=tuple(map(int,item['last_update'].split('/')))
        if mes <10:
            mes='0'+str(mes)
        if dia<10:
            dia='0'+str(dia)
        entry=Conductor(id=id,lat=lat,long=long,last_update=f'{año}/{mes}/{dia}')
        entry.save()
        

def update_database(ruta='https://gist.githubusercontent.com/CesarF/41958f4bc34240b75a83fce876836044/raw/b524588cb979fc6e3ec5a8913ee497d64509e888/locations.json',wait_time=10):
    try:
        while True:
            json_file=cargar_json(ruta=ruta)
            for item in json_file:
                id=item['id']
                lat=item['lat']
                long=item['long']
                mes,dia,año=tuple(map(int,item['last_update'].split('/')))
                if mes <10:
                    mes='0'+str(mes)
                if dia<10:
                    dia='0'+str(dia)
                try:
                    entry=Conductor.objects.get(pk=id)
                except:
                    entry=None
                
                if entry==None:
                    c=Conductor(id=id,lat=lat,long=long,last_update=f'{año}/{mes}/{dia}')
                else:
                    c=entry
                    c.lat=lat
                    c.long=long
                    c.last_update=f'{año}/{mes}/{dia}'
                c.save()
            
            time.sleep(wait_time)

    except Exception as e:
        print(str(e))



json=cargar_json()
json_to_database(json)

thread=Thread(target=update_database)
thread.start()
print('hilo iniciado')