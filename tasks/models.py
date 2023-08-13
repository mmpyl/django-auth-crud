from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# py manage.py makemigrations
# py manage.py migrate

class Task(models.Model):
    title = models.CharField('Title', max_length=250)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecomplete = models.DateTimeField(null=True, blank=True) # que el campo solo es opcional para el administrador
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # modelo recibe self(referencia a clase Task) utiliza como un string retorna la clase self y su atributo title 
    def __str__(self):
        return self.title + ' - by ' + self.user.username