from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    # return HttpResponse('Hola Mundito')
    # title  = 'Hello Wold'
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            "form": UserCreationForm
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:  # errores dentro de la misma vista
                return render(request, 'signup.html', {
                    "form": UserCreationForm,
                    "error": 'Usuario ya existe'
                })
                # return HttpResponse('Usuario ya existe')
                # register user

        return render(request, 'signup.html', {
            "form": UserCreationForm,
            "error": 'Constaseña no coincide'
        })

        # print(request.POST)
        # print('Obteniendo datos')

@login_required
def tasks(request):
    # tasks = Task.objects.all()# Traime todos los campos de la BD en una variable lista
    # Muestra los campos filtrados
    # .objects.filter(user=request.user) filtra por el usuario registrado y logeado
    # datecomplete__isnull=True -> filtra por el campo si es nullo
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    # tasks = Task.objects.all()# Traime todos los campos de la BD en una variable lista
    # Muestra los campos filtrados
    # .objects.filter(user=request.user) filtra por el usuario registrado y logeado
    # datecomplete__isnull=True -> filtra por el campo si es nullo
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=False).order_by('-datecomplete')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            # print(form)
            # Guarda como una instancia de BD. Debeuelve los datos que estan dentro de ese furmulario (commit=False)
            new_task = form.save(commit=False)
            new_task.user = request.user  # (contiene el usuario)
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:  # si falla TaskForm envia el siguiente error
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valide date'
            })

@login_required
def task_detail(request, task_id):
    # rint(task_id)
    # task = Task.objects.get(pk=task_id)
    if request.method == 'GET':
        # tiene que pasarle las tareas (Task), busca por id, usuario y tareas
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        # si esta condicion falla
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # Task hace una nueva instancia del formulario Taskform
            form = TaskForm(request.POST, instance=task)
            form.save()  # Guarda un formulario actualizando
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "Error aactualizando tarea"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecomplete = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('/')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        # print(request.POST) Visualizar que contiene el metodo POST
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña es incorrecto'
            })
        else:
            login(request, user)  # requisito de login y guarda sesion
            return redirect('tasks')
