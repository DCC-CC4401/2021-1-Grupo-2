from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from pichapp.models import User, Room
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django import http


# Create your views here.

def register_user(request):
    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "pichapp/register.html")  # Mostrar el template

    elif request.method == 'POST':  # Si estamos recibiendo el form de registro
        # Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            return HttpResponseRedirect('/register')
            # TODO: mostrar error
        if User.objects.filter(email=email).exists():
            return HttpResponseRedirect('/register')
            # TODO: mostrar error
        email = request.POST['email']

        # Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password, email=email)

        # Redireccionar la página /login
        return HttpResponseRedirect('/login')

    return render(request, "pichapp/register.html")


def login_user(request):
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
            return HttpResponseRedirect('/login')
            # TODO: mostrar error


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
