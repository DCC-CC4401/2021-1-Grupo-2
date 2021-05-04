<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from pichapp.models import User, Room, ActivityCategory
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages


# Create your views here.

@login_required
def create_room(request):
    today = date.today().strftime("%Y-%m-%d")
    if request.method == 'GET':  # Si estamos cargando la página
        # Mostrar el template
        activities: Activities = ActivityCategory.objects.raw('SELECT name, verbose_name FROM pichapp_ActivityCategory')
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
            return HttpResponseRedirect('/')
        else:
            context = {"error": ["Usuario o contraseña incorrecta"]}
            return render(request, "pichapp/login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')


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
    return render(request, "pichapp/working.html")
>>>>>>> dev
