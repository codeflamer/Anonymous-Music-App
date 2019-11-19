from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, Http404
from .models import Album,Song,Newplaylist
from .forms import AlbumForm, UserRegistrationForm, UserLoginForm, SongForm, UserChange, PlaylistForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
import json


lists = ['JPG', 'PNG']
requirements = ['MP3']


def home(request):
    return HttpResponse('<h1>This is  a  response</h1>')


@login_required
def index(request):
    query_value = request.GET.get('q')
    if query_value:
        albums = Album.objects.get_search(query_value).filter(user=request.user)
        songs = Song.objects.get_search(query_value).filter(album__user=request.user)
    else:
        albums = Album.objects.filter(user=request.user)
        songs = []
    favourite_songs = Song.objects.is_favourite(request.user)
    user = request.user
    context = {'albums': albums, 'songs': songs, 'favourites': favourite_songs,'user':user}
    return render(request, 'tutorials/index.html', context)

@login_required
def details(request, number):
    if request.is_ajax():
        if request.method == 'GET':
            result = ''
            song_id = request.GET.get('value')
            song = Song.objects.get(id=song_id)

            if song.is_favourite == True:
                song.is_favourite = False
                result = "<img src= '/static/tutorials/photos/starimage.png'/>"
            else:
                song.is_favourite = True
                result = "<img src='/static/tutorials/photos/star2.jpg'/>"

            song.save()
            data = {'result': result}
            return HttpResponse(json.dumps(data), content_type="application/json")

    obj = get_object_or_404(Album, id=number)
    num_of_songs = len(Song.objects.filter(album_id=number))
    playlist = Newplaylist.objects.first()
    userplaylist = Newplaylist.objects.filter(owner=request.user).order_by('-created_on')
    if len(Newplaylist.objects.all()) == 0:
        playlist = None
    listy = []
    for playlists in Newplaylist.objects.filter(owner=request.user):
        for songs in playlists.songs.all():
            listy.append(songs)
    context = {'object': obj, 'playlist_name': playlist, 'songs': listy, 'playlists': userplaylist, 'length':num_of_songs}
    if obj.user == request.user:
        return render(request, 'tutorials/details.html', context)
    else:
        raise Http404

@login_required
def form(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        file = request.FILES['album_logo']
        file_str = str(file)
        file_split = file_str.split('.')[1]
        if file_split.upper() not in lists:
            context = {'error_messages': 'The images you are uploading must in JPG and PNG only', 'form': form}
            return render(request, 'tutorials/forms.html', context)
        obj.save()
        return redirect(obj.get_absolute_url())
    context = {'form': form}
    return render(request, 'tutorials/forms.html', context)

@login_required
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

@login_required
def delete(request, number):
    obj = get_object_or_404(Album, pk=number)
    obj.delete()
    return redirect('index')


def register(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        object = form.save(commit=False)
        username = request.POST['username']
        password = request.POST['password1']
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

@login_required
def exit(request):
    logout(request)
    return redirect('login')

@login_required
def addtosong(request,number):
    album = get_object_or_404(Album, pk=number)
    form = SongForm(request.POST or None, request.FILES or None)
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
                'error_messages1': 'The music you are uploading must in MP3 .Please check again and upload accorgdinly',
                'form': form,
                'album': album
            }
            return render(request, 'tutorials/addsongs.html', context)
        messages.success(request, 'Song created successfully.')
        obj.save()
        return redirect(obj.get_absolute_url())
    context = {'form': form, 'album': album}
    return render(request, 'tutorials/addsongs.html', context)


@login_required
def deletesong(request,number,song):
    album = get_object_or_404(Album, pk=number)
    song_result = album.song_set.filter(song_title=song).first()
    song_result.delete()
    messages.success(request, 'Song deleted successfully')
    return redirect(song_result.get_absolute_url())


@login_required
def view_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'tutorials/profile.html', context)


@login_required
def edit_profile(request):
    form = UserChange(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        print(request.FILES)
        ist = form.save(commit=False)
        ist.profile.profile_image = request.FILES['profile_image']
        file = request.FILES['profile_image']
        file_str = str(file)
        file_split = file_str.split('.')[1]
        if file_split.upper() not in lists:
            context = {'error_messages': 'The images you are uploading must in JPG and PNG only', 'form': form}
            return render(request, 'tutorials/forms.html', context)

        ist.profile.save()
        ist.save()
        return redirect('view_profile')

    return render(request, 'tutorials/forms.html', {'form': form})


@login_required
def change_password(request):
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        inst = form.save(commit=False)
        print(inst)
        inst.save()
        update_session_auth_hash(request, form.user)
        messages.success(request, 'Password changed Successfully')
        return redirect('view_profile')

    return render(request, 'tutorials/forms.html', {'form': form})


@login_required
def my_playlists(request):
    playlists = Newplaylist.objects.filter(owner=request.user)
    context = {'playlists':playlists}
    return render(request, 'tutorials/playlists.html', context)


@login_required
def create_playlist(request):
    form = PlaylistForm(request.POST or None)
    if form.is_valid():
        inst = form.save(commit=False)
        inst.owner = request.user
        inst.save()
        return redirect('playlist')
    return render(request, 'tutorials/forms.html', {'form': form})


@login_required
def myplaylists_songs(request,playlistname):
    playlist = Newplaylist.objects.get(name=playlistname)
    context = {'playlist': playlist}
    if playlist.owner == request.user:
        return render(request, 'tutorials/playlist_details.html', context)
    else:
        raise Http404


@login_required
def add_or_remove_from_playlist(request, alpha, num, playlist):
    song = Song.objects.get(pk=num)
    print(playlist)
    name_of_playlist = Newplaylist.objects.get(owner=request.user, name=playlist)
    print(name_of_playlist)
    if alpha == 'add':
        Newplaylist.add_to_playlist(request.user, song, name_of_playlist.name)
        messages.success(request, song.song_title + ' added to playlist.')
    elif alpha == 'remove':
        Newplaylist.remove_from_playlist(request.user, song, name_of_playlist.name)
        messages.success(request, 'song removed from playlist')
    return redirect(song.get_absolute_url())