from pichapp.models import Room, ActivityCategory
from datetime import date, datetime
"""
Funciones auxiliares para la vista de busqueda de sala
"""

param_list = ['nombre_actividad', 'nombre_region',
              'nombre_comuna', 'fecha_inicio', 'fecha_final']


def find_param(dict):
    """
    Retorna True si hay algún parámetro válido para filtrar,
    False en caso contrario
    """
    for param in param_list:
        if param in dict and dict[param] != '':
            return True
    return False


def make_params_list(dict):
    """
    Retorna una lista con los parámetros válidos para filtrar
    en dict
    """
    params_list = []
    for param in param_list:
        if param in dict and dict[param] != '':
                params_list.append(param)
    return params_list


def filtrar_salas(dict):
    """
    Retorna un objeto Room con las salas filtradas según las entradas de dict
    """
    L = make_params_list(dict)
    today = date.today().strftime("%Y-%m-%d")
    room = Room.objects.filter(activity_datetime__gte = datetime.fromisoformat(today))

    if 'nombre_actividad' in L:
        activity_object = ActivityCategory.objects.get(
            verbose_name=dict['nombre_actividad'])
        room = room.filter(category = activity_object)
    if 'nombre_region' in L:
        room = room.filter(region = dict['nombre_region'])
    if 'nombre_comuna' in L:
        room = room.filter(comuna = dict['nombre_comuna'])
    if 'fecha_inicio' in L:
        room = room.filter(activity_datetime__gte = datetime.fromisoformat(dict['fecha_inicio']))
    if 'fecha_final' in L:
        room =  room.filter(activity_datetime__lte = datetime.fromisoformat(dict['fecha_final']))
    return room


def make_salas(salas):
    """
    A partir de un objeto rooms, crea la lista de salas
    que se visualizan en la vista de búsqueda
    """
    lista_salas = []
    temp_salas = []
    for sala in salas:
        if len(temp_salas) < 2:
            temp_salas.append(sala)
        else:
            lista_salas.append(temp_salas)
            temp_salas = [sala]
    if len(temp_salas) != 0:
        lista_salas.append(temp_salas)
    return lista_salas


def search_default_context():
    """
    Retorna el contexto que se utiliza por default en la página de 
    busqueda de sala
    """
    today = date.today().strftime("%Y-%m-%d")
    activities: ActivityCategory = ActivityCategory.objects.raw(
        'SELECT name, verbose_name FROM pichapp_ActivityCategory')
    salas = Room.objects #Room.objects.raw('SELECT * FROM pichapp_Room')
    salas = salas.filter(activity_datetime__gte = datetime.fromisoformat(today)) #Room.objects.raw('SELECT * FROM pichapp_Room')
    lista_salas = make_salas(salas)

    context = {
        'fecha': today,
        'activities': activities,
        'lista_salas': lista_salas
    }
    return context
