from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseNotFound
from datetime import date

# Create your views here.

today = date.today().strftime("%Y-%m-%d")

def crear_sala(request):
    if request.method == 'GET':  # Si estamos cargando la página
        return render(request, "crear_sala.html", {'fecha': today})  # Mostrar el template

    if request.method == 'POST': #Estamos creando la sala (enviando el formulario)

        nombre_cancha = request.POST["nombre_cancha"]
        nombre_comuna = request.POST["nombre_comuna"]
        nombre_region = request.POST["nombre_region"]
        nombre_actividad = request.POST["nombre_actividad"]
        fecha = request.POST["fecha"]
        hora_encuentro = request.POST["hora_encuentro"]
        tamano_sala = request.POST["tamano_sala"]
        anfitrion = request.user.username #Obtenemos el nombre de usuario del anfitrión


        return HttpResponseRedirect('/_sala')
