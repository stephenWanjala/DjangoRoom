from django.shortcuts import render, redirect

from .forms import RoomForm
from .models import Room


# rooms = [
#     {'id': 1, 'name': "Python"},
#     {'id': 2, 'name': "Design with me"},
#     {'id': 3, 'name': "Core draw beginners"},
#
# ]


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    context = {'rooms': rooms}
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
