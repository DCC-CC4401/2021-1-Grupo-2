
# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


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
        upload_to='pichapp/media',
        null=True
    )


class Room(models.Model):
    creation_date = models.DateTimeField(
        verbose_name='Fecha de creación',
        auto_now_add=True
    )
    participants = models.ManyToManyField(
        User,
        related_name='rooms',
        blank=True
    )
    name = models.CharField(
        max_length=255
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
        default=1
    )
    max_size = models.IntegerField(
        verbose_name='Participantes máximos'
    )
    region = models.CharField(
        verbose_name='Región',
        max_length=255
    )
    comuna = models.CharField(
        verbose_name='Comuna',
        max_length=255
    )
    meeting_place = models.CharField(
        verbose_name='Lugar de encuentro',
        max_length=255
    )
    activity_datetime = models.DateTimeField(
        verbose_name='Fecha del encuentro',
    )

    @property
    def is_full(self):
        return self.current_size >= self.max_size

    @property
    def place(self):
        return f"{self.meeting_place} ({self.region}/{self.comuna})"


class RoomMessage(models.Model):
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    content = models.TextField(
        verbose_name="Contenido"
    )
    creation_date = models.DateTimeField(
        verbose_name="Fecha de creación",
        auto_now_add=True
    )


@receiver(m2m_changed, sender=Room.participants.through)
def on_participants_changed(instance: Room, action: str, **kwargs):
    print("OLA")
    if action in ['post_add', 'post_remove', 'post_clear']:
        size = instance.participants.count()
        instance.current_size = size
        instance.is_open = size < instance.max_size
        instance.save()
