from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, Topic
from .forms import RoomForm


# Create your views here.
def home(request):
    rooms = Room.objects.all()
    topics = Topic.objects.all()
    context = {
        "rooms":rooms,
        "topics":topics,
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
            "room":room
        }
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {
        "form":form
    }
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        "form":form
    }
    return render(request,'base/room_form.html', context )

def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    room.delete()
    return redirect('home')