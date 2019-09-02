from django.shortcuts import render, HttpResponse,get_object_or_404,redirect, Http404
from .models import Album,Song
from django.views import generic
from .forms import AlbumForm,UserRegistrationForm,UserLoginForm,SongForm
from django.contrib.auth import login,logout,authenticate
from .serializers import AlbumSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


lists = ['JPG','PNG']
requirements = ['MP3','MP4']

def home(request):
    return HttpResponse('<h1>This is  a  response</h1>')


def index(request):
    query_value = request.GET.get('q')
    if query_value:
        albums = Album.objects.get_search(query_value).filter(user=request.user)
        songs = Song.objects.get_search(query_value).filter(album__user=request.user)
    else:
        albums = Album.objects.filter(user=request.user)
        songs = []
    favourite_songs = Song.objects.is_favourite(request.user)
    context = {'albums': albums, 'songs': songs, 'favourites': favourite_songs}
    return render(request, 'tutorials/index.html', context)

def details(request,number):

    obj = get_object_or_404(Album, id=number)
    context = {'object': obj}

    if obj.user == request.user:
        return render(request, 'tutorials/details.html', context)
    else:
        raise Http404

def form(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        file = request.FILES['album_logo']
        file_str = str(file)
        file_split = file_str.split('.')[1]
        if file_split.upper() not in lists:
            context = {'error_messages': 'The images you are uploading must in JPG only', 'form': form}
            return render(request, 'tutorials/forms.html', context)
        obj.save()
        return redirect(obj.get_absolute_url())
    context = {'form': form}
    return render(request, 'tutorials/forms.html', context)


def update(request, number):
    value = get_object_or_404(Album, pk=number)
    previous_logo = value.album_logo
    form = AlbumForm(request.POST or None,  request.FILES or None, instance=value)
    if form.is_valid():
        obj = form.save(commit=False)
        if 'album_logo' not in request.FILES:
            obj.album_logo = previous_logo
            obj.save()
            return redirect(obj.get_absolute_url())
        else:
            file = request.FILES['album_logo']
            file_str = str(file)
            file_split = file_str.split('.')[1]
            if file_split.upper() not in lists:
                context = {'error_messages':'The images you are uploading must in JPG only', 'form': form}
                return render(request, 'tutorials/forms.html', context)
            obj.save()
            return redirect(obj.get_absolute_url())
    context = {'form': form}
    return render(request, 'tutorials/forms.html', context)

def delete(request,number):
    object = get_object_or_404(Album, pk=number)
    object.delete()
    return redirect('index')

def register(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        object = form.save(commit=False)
        username = request.POST['username']
        password = request.POST['password']
        object.set_password(password)
        object.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
    return render(request, 'tutorials/forms.html', {'form': form})

def comein(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
            else:
                context = {
                    'form': form,
                    'error_messages': 'Your account is not active,Please contact the admin..'
                }
                return render(request, 'tutorials/forms.html', context)
        else:
            context = {
                       'form':form,
                       'error_messages': 'You are not Entitled to login.Please check username and password.',
                       }
            return render(request, 'tutorials/forms.html', context)
    return render(request, 'tutorials/forms.html', {'form': form})

def exit(request):
    logout(request)
    return redirect('login')

def addtosong(request,number):
    album = get_object_or_404(Album, pk=number)
    form = SongForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.album = album
        file = request.FILES['real_song']
        file_str = str(file)
        file_split = file_str.split('.')[1]
        songtitleinputed = request.POST['song_title']
        query_set = album.song_set.filter(song_title=songtitleinputed)

        if query_set.exists():
            context = {'form': form, 'error_message': 'This song already exists in this album.', 'album': album}
            return render(request, 'tutorials/addsongs.html', context)

        if file_split.upper() not in requirements:
            context = {
                'error_messages1': 'The music you are uploading must in MP3 or MP4.Please check again and upload accorgdinly',
                'form': form,
                'album': album
            }
            return render(request, 'tutorials/addsongs.html', context)
        obj.save()
        return redirect(obj.get_absolute_url())
    context = {'form': form, 'album': album}
    return render(request, 'tutorials/addsongs.html', context)


def deletesong(request,number,song):
    album = get_object_or_404(Album, pk=number)
    song_result = album.song_set.filter(song_title=song).first()
    song_result.delete()
    return redirect(song_result.get_absolute_url())








class IndexView(generic.ListView):
    template_name = 'tutorials/first.html'
    context_object_name = 'all_albums'
    def get_queryset(self):
        return Album.objects.all()

class DetailView(generic.DetailView):
    template_name = 'tutorials/second.html'
    model = Album

class AlbumList(APIView):

    def get(self,request):
        albums = Album.objects.all()
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data)

    def post(self):
        pass