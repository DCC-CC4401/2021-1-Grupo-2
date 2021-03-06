import json
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from pichapp.models import RoomMessage, User, Room, ActivityCategory
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from pichapp.aux_modules.search_room import *
from django.db.models import Count

# Create your views here.

@login_required
def search_room(request):
    if request.method == 'GET':
        print(request.GET)
        if 'filtrar' in request.GET:  # Caso el llamado GET es dado por el botón de filtrar
            today = date.today().strftime("%Y-%m-%d")
            activities: ActivityCategory = ActivityCategory.objects.raw(
                'SELECT name, verbose_name FROM pichapp_ActivityCategory')
            # Se busca si hay algún parámetro que valga la pena filtrar
            found_param = find_param(request.GET)

            if found_param:
                salas = filtrar_salas(request.GET)
                print(salas)

            else:
                salas = filtrar_salas(request.GET)
                #salas = Room.objects.raw('SELECT * FROM pichapp_Room')

            lista_salas = make_salas(salas)
            
            context = {
                'fecha': today,
                'activities': activities,
                'lista_salas': lista_salas
            }

            return render(request, "pichapp/room/search_room.html", context)
        # Página por default
        else:
            context = search_default_context()
            return render(request, "pichapp/room/search_room.html", context)

    if request.method == 'POST':
        numero_sala = request.POST["numero_sala"]
        sala_encontrada = Room.objects.raw(
            'SELECT id FROM pichapp_Room WHERE id =' + numero_sala)
        for p in sala_encontrada:
            if p.id == int(numero_sala):
                return HttpResponseRedirect('/rooms/' + numero_sala + '/')
        # Falla la busqueda por id, se retorna la página por default
        # junto a mensaje de error
        context = search_default_context()
        context['error'] = ["Id de la sala inexistente"]
        return render(request, "pichapp/room/search_room.html", context)


@login_required
def create_room(request):
    today = date.today().strftime("%Y-%m-%d")
    if request.method == 'GET':  # Si estamos cargando la página
        # Mostrar el template
        activities: ActivityCategory = ActivityCategory.objects.raw(
            'SELECT name, verbose_name FROM pichapp_ActivityCategory')
        print(activities)
        context = {
            'fecha': today,
            'activities': activities
        }
        return render(request, "pichapp/room/create_room.html", context)

    # Estamos creando la sala (enviando el formulario)
    if request.method == 'POST':

        nombre_sala = request.POST["nombre_sala"]
        nombre_lugar = request.POST["nombre_lugar"]
        nombre_comuna = request.POST["nombre_comuna"]
        nombre_region = request.POST["nombre_region"]
        nombre_actividad = request.POST["nombre_actividad"]
        print(nombre_actividad)
        activity_object = ActivityCategory.objects.get(
            verbose_name=nombre_actividad)

        fecha = request.POST["fecha"]
        hora_encuentro = request.POST["hora_encuentro"]
        tamano_sala = int(request.POST["tamano_sala"])
        anfitrion = request.user  # Obtenemos el nombre de usuario del anfitrión

        room = Room.objects.create(name=nombre_sala, host=anfitrion, category=activity_object,
                                   max_size=tamano_sala, region=nombre_region,
                                   comuna=nombre_comuna, meeting_place=nombre_lugar,
                                   activity_datetime=datetime.fromisoformat(fecha + "T" + hora_encuentro))
        room.participants.add(anfitrion)

        room.save()  # Guardamos la sala en la base
        pk = room.id

        return HttpResponseRedirect('/rooms/'+str(pk))


def register_user(request):
    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "pichapp/register.html")  # Mostrar el template

    elif request.method == 'POST':  # Si estamos recibiendo el form de registro
        # Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        context = {"error": []}

        if User.objects.filter(username=username).exists():
            context["error"].append("El usuario ya está en uso")
        if User.objects.filter(email=email).exists():
            context["error"].append("El email ya está en uso")

        if len(context["error"]) > 0:
            return render(request, "pichapp/register.html", context)

        # Crear el nuevo usuario
        user = User.objects.create_user(
            username=username, password=password, email=email)
        messages.add_message(request, messages.INFO,
                             "Usuario creado correctamente")

        # Redireccionar la página /login
        return HttpResponseRedirect("/login", context)

    return render(request, "pichapp/register.html")


def login_user(request):

    storage = messages.get_messages(request)
    success = None
    for message in storage:
        success = message
        return render(request, 'pichapp/login.html', {'success': success})

    if request.method == 'GET':
        return render(request, "pichapp/login.html")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home')
        else:
            context = {"error": ["Usuario o contraseña incorrecta"]}
            return render(request, "pichapp/login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def room_detail(request, pk: int):
    if request.method == 'GET':
        room: Room = get_object_or_404(Room, pk=pk)
        user: User = request.user
        context = {
            'room': room,
            'is_authenticated': False,
            'in_room': False,
        }
        if user.is_authenticated:
            context['is_authenticated'] = True
            context['user'] = user
            if room.participants.filter(username=user.username).count() > 0:
                context['in_room'] = True
        return render(request, "pichapp/room_detail.html", context)


def room_chat_messages(request, pk: int):
    user: User = request.user;
    room: Room = get_object_or_404(Room, pk=pk)
    if request.method == 'GET':
        queryset = RoomMessage.objects.filter(
                room=room
            ).order_by(
                '-creation_date'
            )
        messages = map(lambda m: {
            "id": m.id,
            "user": {
                "name": m.user.username,
            },
            "content": m.content,
            "creation_date": m.creation_date,
        }, queryset)
        messages = list(messages)
        return JsonResponse({
            "messages": messages,
        })
    elif request.method == 'POST':
        if not user.is_authenticated:
            return HttpResponseNotAllowed()
        data = json.loads(request.body)
        if not 'content' in data:
            return HttpResponseBadRequest()
        content = data['content']
        RoomMessage.objects.create(
            room=room,
            user=user,
            content=content
        )
        return HttpResponse(status=201)
        

@login_required
def join_room(request, pk: int):
    if request.method == 'POST':
        room: Room = get_object_or_404(Room, pk=pk)
        room.participants.add(request.user)
        room.save()
        return HttpResponseRedirect(f'/rooms/{pk}')


@login_required
def exit_room(request, pk: int):
    if request.method == 'POST':
        room: Room = get_object_or_404(Room, pk=pk)
        room.participants.remove(request.user)
        room.save()
        return HttpResponseRedirect(f'/rooms/{pk}')


@login_required
def home_view(request):
    best_rooms = Room.objects.values('category').annotate(total=Count('category')).order_by('-total').all()[:3]
    best_rooms_context = []
    for category in best_rooms:
        best_rooms_context.append(ActivityCategory.objects.filter(name=category["category"])[0])
    sports = ActivityCategory.objects.all()
    are_rooms = False
    if len(best_rooms_context) > 0:
        are_rooms = True
    sports_context = [sports[x:x+4] for x in range(0, len(sports), 4)]
    if len(sports_context) % 4 != 0:
        sports_context[len(sports) // 4] = [False] + sports_context[len(sports) // 4] +[False]
    context = {
        "best_rooms" : best_rooms_context,
        "sports" : sports_context,
        "are_b_rooms" : are_rooms,
        "best_rooms_numbers" : [x + 1 for x in range(len(best_rooms_context))]
    }
    return render(request, "pichapp/home.html", context)

def landing_view(request):
    if not request.user.is_authenticated:
        return render(request, "pichapp/landing.html")
    else:
        return home_view(request)
