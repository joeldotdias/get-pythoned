from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth
from .forms import SignUpForm, LoginForm
from dotenv import load_dotenv
from .helpers import get_token, get_song_by_genre

# Create your views here.

def home_page(request):
    load_dotenv()
    vec = [1, 2,3,4,5,6,7,8,9,10,11,12,13,14]
    return render(request, 'pages/landing.html', {'history': vec})

def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('/')
        
    
    return render(request, 'pages/login.html', context={'loginform':form})


def signup_page(request):
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    
    return render(request, 'pages/signup.html', context={'signupform':form})


def mood_page(request):
    token = get_token()
    mood = request.GET.get('type')
    genres = ""
    if mood == "happy":
        genres = "happy,pop,road-trip"
    elif mood == "sad":
        genres = "sad,emo,indie-pop"
    elif mood == "turnt":
        genres = "hip-hop,drum-and-bass,hard-rock"
    elif mood == "mellow":
        genres = "country,road-trip,chill"
    else:
        genres == "happy,sad,hip-hop,country"

    tracks = get_song_by_genre(token, genres)
    return render(request, 'pages/mood.html', { 'tracks': tracks })


def user_logout(request):
    auth.logout(request)
    return redirect('/')