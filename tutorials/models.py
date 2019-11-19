from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import post_save
from django.shortcuts import redirect

AUDIO_FORMAT = (
        ('MPEG3', 'MP3'),
        ('MPEG4', 'MP4')
    )

class customqueryset(models.query.QuerySet):
    def search(self, query):
        lookups = (
            Q(artist__icontains=query)|
            Q(album_title__icontains=query)|
            Q(genre__icontains=query)|
            Q(genre__icontains=query)
        )
        return self.filter(lookups).distinct()

class SearchModelManager(models.Manager):
    def get_queryset(self):
        return customqueryset(self.model,using=self.db)

    def get_search(self,query):
        return self.get_queryset().search(query)



class customsongqueryset(models.query.QuerySet):
    def search(self, query):
        lookups = (
            Q(file_type__icontains=query)|
            Q(song_title__icontains=query)
        )
        return self.filter(lookups).distinct()

class SearchSongModelManager(models.Manager):
    def get_queryset(self):
        return customsongqueryset(self.model,using=self.db)

    def get_search(self, query):
        return self.get_queryset().search(query)

    def is_favourite(self, userid):
        return self.filter(is_favourite=True).filter(album__user=userid)



class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    artist = models.CharField(max_length=100,help_text='Enter your artist name here')
    album_title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField(upload_to='media')
    objects = SearchModelManager()

    def get_absolute_url(self):
        return reverse('details', kwargs={'number': self.id})

    @property
    def length(self):
        return len(self.song_set.all())

    def __str__(self):
        return self.album_title + '-' + self.artist


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    real_song = models.FileField(upload_to='music', default='/media/music/leesun.mp3', help_text='Hint: Files must be MP3 or MP4')
    file_type = models.CharField(choices=AUDIO_FORMAT, default='MPEG3', max_length=100)
    song_title = models.CharField(max_length=100)
    is_favourite = models.BooleanField(default=False)
    objects = SearchSongModelManager()

    def get_absolute_url(self):
        return reverse('details', kwargs={'number': self.album.id})

    def __str__(self):
        return self.song_title


class Newplaylist(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @classmethod
    def add_to_playlist(cls, owner, new_song, name):
        name, created = cls.objects.get_or_create(
            owner=owner, name=name
        )
        name.songs.add(new_song)

    @classmethod
    def remove_from_playlist(cls, owner, songs, name):
        name, created = cls.objects.get_or_create(
            owner=owner, name=name
        )
        name.songs.remove(songs)

    def __str__(self):
        return self.name+'--'+self.owner.username



class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    profile_image = models.FileField(default='anonymous1.png')

    def __str__(self):
        return self.user.username



def create_profile(sender,**kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile,sender=User)