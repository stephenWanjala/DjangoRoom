from django.shortcuts import render

rooms = [
    {'id': 1, 'name': "Python"},
    {'id': 2, 'name': "Design with me"},
    {'id': 3, 'name': "Core draw beginners"},

]


# Create your views here.
def home(request):
    context = {'rooms': rooms}
    return render(request, template_name="base/home.html", context=context)


def room(request, pk):
    context_room = None
    for i in rooms:
        if i['id'] == int(pk):
            context_room = i
    return render(request, template_name="base/room.html", context={'room': context_room})
