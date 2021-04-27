from django.shortcuts import render
from pichapp.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
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
