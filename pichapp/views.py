from django.shortcuts import render
from pichapp.models import User

# Create your views here.

def register_user(request):
    if request.method == 'GET': #Si estamos cargando la página
        return render(request, "pichapp/register.html") #Mostrar el template

    elif request.method == 'POST': #Si estamos recibiendo el form de registro
     #Tomar los elementos del formulario que vienen en request.POST
        username = request.POST['username']
        password = request.POST['password']
        #apodo = request.POST['apodo']
        #pronombre = request.POST['pronombre']
        email = request.POST['email']

        #Crear el nuevo usuario
        user = User.objects.create_user(username=username, password=password, email=email)

     #Redireccionar la página /tareas
        return HttpResponseRedirect('/tareas')

    return render(request,"pichapp/register.html")
