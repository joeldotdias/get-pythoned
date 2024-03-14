from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'pages/landing.html')

def mood_page(request):
    print(request.GET.get('type'))
    return render(request, 'pages/mood.html')