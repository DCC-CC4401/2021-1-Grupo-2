from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    # pronombres = [('La', 'La'), ('El', 'El'), ('Le', 'Le'), ('Otro', 'Otro')]
    # pronombre = models.CharField(max_length=5,choices=pronombres)
    # apodo = models.CharField(max_length=30)
    # TODO: user extra atributes


class ActivityCategory(models.Model):
    name = models.CharField(
        verbose_name='Nombre de código',
        max_length=255,
        primary_key=True
    )
    verbose_name = models.CharField(
        verbose_name='Nombre',
        max_length=255
    )
    image = models.ImageField(
        verbose_name='Imagen',
        null=True
    )


class Room(models.Model):
    # TODO: make this model auto add the host to `participants` field
    #       when a new instance is created
    # TODO: make this model auto update `is_active` field
    #       whenever the participants relationship is changed
    #       see: https://docs.djangoproject.com/en/3.2/ref/signals/#m2m-changed
    creation_date = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='rooms',
        blank=True
    )
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='hosted_rooms'
    )
    category = models.ForeignKey(
        ActivityCategory,
        on_delete=models.CASCADE,
    )
    is_active = models.BooleanField(
        verbose_name='Está activo',
        default=True
    )
    is_open = models.BooleanField(
        verbose_name='Está abierto',
        default=True
    )
    current_size = models.IntegerField(
        verbose_name='Participantes actuales',
        default=0
    )
    max_size = models.IntegerField(
        verbose_name='Participantes máximos'
    )
    place = models.CharField(
        verbose_name='Lugar',
        max_length=255
    )
    activity_datetime = models.DateTimeField(
        verbose_name='Fecha del encuentro',
    )
