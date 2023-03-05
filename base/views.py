from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room, Topic, Message


# rooms = [
#     {'id': 1, 'name': "Python"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Core draw beginners"},
#
# ]

def login_page(request):
    page_name = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username').lower()
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
    context = {'page': page_name}
    return render(request, 'base/login_register.html', context=context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    # page_name = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('home')
        else:
            messages.error(request, "An error Occurred During Registration")
    context = {'form': form}
    return render(request, 'base/login_register.html', context=context)


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
    participants = context_room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(user=request.user, room=context_room, body=request.POST.get('body'))
        context_room.participants.add(request.user)
        return redirect('room', pk=context_room.id)
    room_messages = context_room.message_set.all().order_by('-created')
    context = {'room': context_room, 'room_messages': room_messages, 'participants': participants}
    return render(request, template_name="base/room.html", context=context)


@login_required(login_url='login')
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


@login_required(login_url='login')
def update_room(request, pk):
    room_to_update = Room.objects.get(id=pk)
    form = RoomForm(instance=room_to_update)
    if request.user != room_to_update.host:
        return HttpResponse("Not Allowed here")
    if request.method == 'POST':
        print(request.POST)
        form = RoomForm(request.POST, instance=room_to_update)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/room_form.html', context=context)


@login_required(login_url='login')
def delete_room(request, pk):
    room_to_delete = Room.objects.get(id=pk)
    if request.user != room_to_delete.host:
        return HttpResponse("Only the creator of the room can delete room")
    if request.method == 'POST':
        room_to_delete.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={'obj': room})


@login_required(login_url='login')
def delete_message(request, pk):
    message_to_delete = Message.objects.get(id=pk)
    if request.user != message_to_delete.user:
        return HttpResponse("Only the creator of the message can delete message")
    if request.method == 'POST':
        message_to_delete.delete()
        return redirect('home')
    return render(request, 'base/delete.html', context={'obj': message_to_delete})
