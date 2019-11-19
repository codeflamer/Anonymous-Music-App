from django.contrib.auth.models import User
from django import forms
from .models import Album,Song,Newplaylist
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['artist','album_title','genre','album_logo']

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Newplaylist
        fields = ['name']

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     user = User.objects.filter(email=email)
    #     if user.exists:
    #         raise forms.ValidationError('emailaddress already exists.')

class UserChange(UserChangeForm):
    profile_image = forms.FileField()
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'profile_image'
        )



class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ['username', 'password']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['file_type', 'real_song', 'song_title', 'is_favourite']