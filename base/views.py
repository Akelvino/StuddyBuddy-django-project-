from django.shortcuts import render

# Create your views here.
rooms = [
    {'id':1, 'name':"Learn to code"},
    {'id':2, 'name':"Learn to code python programing"},
    {'id':3, 'name':"Learn to python framework django"}
]



def home(request):
    return render(request, 'base/home.html', {"rooms":rooms})

def room(request):
    return render(request, 'base/room.html')