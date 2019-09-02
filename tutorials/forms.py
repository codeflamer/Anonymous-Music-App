from django.contrib.auth.models import User
from django import forms
from .models import Album,Song

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist','album_title','genre','album_logo']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['file_type', 'real_song', 'song_title', 'is_favourite']