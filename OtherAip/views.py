from django.shortcuts import render,HttpResponse

# Create your views here.
import deezer
import json
import requests



def Others(request):
    client = deezer.Client(app_id='foo', app_secret='bar')
    song = client.advanced_search({"artist": "Rihanna"})[6]
    context = {'values': song}

    return render(request, 'OtherAip/AllCollection.html', context)
