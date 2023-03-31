from django.shortcuts import render, redirect, get_object_or_404
from .models import room, topic, message, User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import roomForm, messForm, UserForm, MyUserCreateForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

# rooms = [
#     {'id': 1, 'name': "room 1"},
#     {'id': 2, 'name': "room 2"},
#     {'id': 3, 'name': "room 3"}
# ]


def loginPage(request):
    
    page ='login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email= email)
        except:
            messages.error(request, 'user is not exist!')

        else:
            user = authenticate(request, email= email, password= password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Username or Password does not exist')
        
    return render(request, 'base/login.html', {'page': page})

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreateForm

    if request.method == 'POST':
        form = MyUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        
        else :
            messages.error(request, 'an error occurred during registration ')

    context = {'form':form}
    return render(request, 'base/signup.html', context)

def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = room.objects.filter(
        Q(topic__name__icontains= q) |
        Q(name__icontains= q) |
        Q(host__username__icontains= q) |
        Q(description__icontains= q)
    )

    topics = topic.objects.all()[:5]
    room_count = rooms.count()
    room_msg = message.objects.filter(
        Q(room__topic__name__icontains=q) |
        Q(user__username__icontains=q) |
        Q(room__name__icontains=q)
    )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_message': room_msg}
    return render(request, "base/home.html" , context)

def roomView(request, pk):
    p_room = room.objects.get(pk=pk)
    room_messages = message.objects.filter(room= p_room)
    participants = p_room.participants.all()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('loginRegister')
        
        comment = str(request.POST.get('comment')).strip()
        if comment:
            message.objects.create(room= p_room, user= request.user, body= comment)
            p_room.participants.add(request.user)

    context = {'room': p_room, 'room_messages':room_messages, 'participants':participants}

    return render(request, "base/room.html", context)

def userProfile(request, pk):
    user = User.objects.get(pk=pk)
    rooms = user.room_set.all()
    topics = topic.objects.all()
    room_msg = user.message_set.all()

    context = {'user': user,'rooms': rooms, 'topics': topics, 'room_message': room_msg}
    return render(request, 'base/profile.html', context)

@login_required(login_url='loginRegister')
def create_room(request):
    form = roomForm()
    topics = topic.objects.all()
    
    if request.method == 'POST':
        tp_name = request.POST.get('topic')
        tp, created = topic.objects.get_or_create(name= tp_name)

        room.objects.create(
            host = request.user,
            topic = tp,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        
        return redirect('home')

    context = {"form": form , 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='loginRegister')
def update_room(request, pk):
    p_room = room.objects.get(pk=pk)
    form = roomForm(instance=p_room)
    topics = topic.objects.all()

    if request.user != p_room.host:
        return HttpResponse('You are not allow here')

    if request.method == 'POST':
        tp_name = request.POST.get('topic')
        tp , created = topic.objects.get_or_create(name= tp_name)
        
        p_room.topic = tp
        p_room.description = request.POST.get('description')
        p_room.name = request.POST.get('name')
        p_room.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': p_room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='loginRegister')
def delete_room(request , pk):
    p_room = room.objects.get(pk = pk)

    if request.user != p_room.host:
        return HttpResponse('You are not allow here')
    
    if request.method == 'POST':
        p_room.delete()
        return redirect('home')
    
    context = {'obj': p_room}
    return render(request, 'base/delete_form.html', context)

@login_required(login_url='loginRegister')
def delete_message(request , pk):
    room_mesg = message.objects.get(pk = pk)
    if request.user != room_mesg.user:
        return HttpResponse('You are not allow here')
    
    if request.method == 'POST':
        room_mesg.delete()
        return redirect('room', room_mesg.room.id)
    
    context = {'obj': room_mesg}
    return render(request, 'base/delete_form.html', context)

@login_required(login_url='loginRegister')
def update_message(request, pk):
    msg = message.objects.get(pk=pk)
    msg_form = messForm(instance=msg)

    if request.user != msg.user:
        return HttpResponse('You are not allow here')

    if request.method == 'POST':
        msg_form = messForm(request.POST , instance=msg)
        if msg_form.is_valid():
            msg_form.save()
            return redirect('room', msg.room.id)

    context = {'form': msg_form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='loginRegister')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile' , user.id)
    
    return render(request, 'base/update_user.html', {'form': form})

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = topic.objects.filter(name__icontains = q)

    return render(request, 'base/topics.html' , {"topics" : topics})
 

def activityPage(request):
    room_msg = message.objects.all()
    context = {'room_message': room_msg}
    return render(request, 'base/activity.html' , context)