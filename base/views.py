from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic


# rooms = [
#     {'id': 1, 'name': "Python"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Core draw beginners"},
#
# ]

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exit")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist")
    context = {}
    return render(request, 'base/login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('home')


# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q)
        | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, template_name="base/home.html", context=context)


def room(request, pk):
    context_room = Room.objects.get(id=pk)
    return render(request, template_name="base/room.html", context={'room': context_room})


def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room_to_update = Room.objects.get(id=pk)
    form = RoomForm(instance=room_to_update)
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST, instance=room_to_update)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context=context)


def delete_room(request, pk):
    room_to_delete = Room.objects.get(id=pk)
    if request.method == 'POST':
        room_to_delete.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={'obj': room})
