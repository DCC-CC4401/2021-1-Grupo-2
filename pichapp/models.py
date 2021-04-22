from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    #pronombres = [('La','La'),('El','El'), ('Le','Le'),('Otro','Otro')]
    #pronombre = models.CharField(max_length=5,choices=pronombres)
    #apodo = models.CharField(max_length=30)
    # TODO: user extra atributes