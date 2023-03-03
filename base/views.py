from django.shortcuts import render

rooms = [
    {'id': 1, 'name': "Python"},
    {'id': 2, 'name': "Design with me"},
    {'id': 3, 'name': "Core draw beginners"},

]


# Create your views here.
def home(request):
    context = {'rooms': rooms}
    return render(request, template_name="home.html", context=context)


def room(request):
    return render(request, template_name="room.html", )
