# Generated by Django 3.2 on 2021-06-18 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pichapp', '0007_auto_20210429_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='current_size',
            field=models.IntegerField(default=1, verbose_name='Participantes actuales'),
        ),
    ]
