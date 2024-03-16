from django.shortcuts import render
from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

# Create your views here.

def home_page(request):
    load_dotenv()
    return render(request, 'pages/landing.html')

def mood_page(request):
    token = get_token()
    tracks = get_song_by_genre(token, "house")
    print(request.GET.get('type'))
    return render(request, 'pages/mood.html', { 'tracks': tracks })


def get_song_by_genre(token, genre):
    url = f"https://api.spotify.com/v1/recommendations?seed_genres={genre}&country=IN"
    headers = get_auth_header(token)
    res = get(url, headers=headers)
    json_res = json.loads(res.content)
    gotten =  json_res["tracks"]
    returnable = []
    for tr in gotten:
        name =  tr["name"]
        album = tr["album"]["name"]
        artists = []
        for ar in tr["artists"]:
            artists.append(ar["name"])
        url = tr["external_urls"]["spotify"]
        imgUrl = tr["album"]["images"][0]["url"]
        returnable.append(TrackDetails(name, ", ".join(artists), album, url, imgUrl))
    return returnable


class TrackDetails:
    def __init__(self, name, artists, album, url, imgUrl):
        self.name = name
        self.artists = artists
        self.album = album
        self.url = url
        self.imgUrl = imgUrl

def get_token():
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    auth_str = client_id + ":" + client_secret
    auth_bytes = auth_str.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers = headers, data = data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return { "Authorization": "Bearer " + token }

