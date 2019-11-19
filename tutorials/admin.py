from django.contrib import admin
from .models import Album, Song, Newplaylist,Profile


class AlbumModel(admin.ModelAdmin):
    list_display = ['album_title', 'user', 'artist', 'genre']

    class Meta:
        model = Album
        fields = [
            'album_title',
            'user',
            'artist',
            'genre'
        ]




admin.site.register(Album,AlbumModel)
admin.site.register(Song)
admin.site.register(Newplaylist)
admin.site.register(Profile)
# Register your models here.
