from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth
from django.views.decorators.csrf import csrf_exempt

from dotenv import load_dotenv
from .forms import SignUpForm, LoginForm
from .helpers import get_token, get_song_by_genre
from .models import HistTrack



def home_page(request):
    load_dotenv()
    history = []
    
    if request.user.is_authenticated:
        curr_user = request.user.username
        history = HistTrack.objects.filter(user_id=curr_user)
        
    return render(request, 'pages/landing.html', {'history': history})

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
    # apologies for such shitty code but putting this in a dict gives the wierdest errors
    # perhaps my dict isn't big enough
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

@csrf_exempt
def add_song(request):
    title = request.GET.get('title')
    img_url = request.GET.get('img')
    url = request.GET.get('spurl')
    
    if request.user.is_authenticated:
        curr_user = request.user.username
        HistTrack.objects.create(user_id=curr_user, title=title, url=url, img_url=img_url)