from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from pichapp.models import User, Room
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.

def register_user(request):
    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "pichapp/register.html")  # Mostrar el template

    elif request.method == 'POST':  # Si estamos recibiendo el form de registro
        # Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        context = {"error":[]}

        if User.objects.filter(username=username).exists():
            context["error"].append("El usuario ya está en uso")
        if User.objects.filter(email=email).exists():
            context["error"].append("El email ya está en uso")
        
        if len(context["error"]) > 0:
            return render(request, "pichapp/register.html", context)

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password, email=email)
        messages.add_message(request, messages.INFO, "Usuario creado correctamente")

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
            context = {"error" : ["Usuario o contraseña incorrecta"]}
            return render(request, "pichapp/login.html", context)


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/home')


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
