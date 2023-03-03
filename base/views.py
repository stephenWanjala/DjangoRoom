from django.shortcuts import render

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
