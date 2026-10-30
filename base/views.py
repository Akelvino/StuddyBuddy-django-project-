from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Topic, Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def logInPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get("username").lower()
        password = request.POST.get("password")
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,"User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have loged in successfully")
            return redirect('home')
        else:
            messages.error(request, "Username does not exist")
        

    context = {"page":page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    context ={"form":form}
    return render(request, 'base/login_register.html', context)



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(description__icontains =q)|
        Q(name__icontains=q)
    )
    rmessages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )
    room_count = rooms.count
    topics = Topic.objects.all()
    context = {
        "rooms":rooms,
        "topics":topics,
        "room_count":room_count,
        "rmessages":rmessages
    }
    return render(request, 'base/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    rmessages = room.message_set.all().order_by('-created')
    participants = room.participants.filter()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {
            "room":room,
            "rmessages":rmessages,
            "participants":participants
        }
    return render(request, 'base/room.html', context)

@login_required(login_url = 'login')
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

@login_required(login_url = 'login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        messages.error(request, "You are not allowed hear!!!")
        return redirect('home')

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        "form":form
    }
    return render(request,'base/room_form.html', context )

@login_required(login_url = 'login')
def deleteRoom(request, pk):
    room = get_object_or_404(Room, id=pk)
    if request.user != room.host:
        messages.error(request, "You are not allowed to delete!!!")
        return redirect('home')
    else:
        room.delete()
        return redirect('home')

@login_required(login_url='login')
def deleteMessage(requst,pk):
    message = get_object_or_404(Message, id=pk)
    room_id = message.room.id
    message.delete()
    return redirect('room', pk=room_id)