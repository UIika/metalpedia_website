from django.contrib import admin
from .models import *

# Register your models here.

class BandAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name','found_year')
    
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
    
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'release_year')
    ordering = ('name',)
    search_fields = ('name', 'release_year')
    
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name',)
    search_fields = ('name', )
    list_filter = ('album',)
    
class YearAdmin(admin.ModelAdmin):
    list_display = ('number', )
    ordering = ('number',)
    
class ProfessionAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ('name',)

admin.site.register(Band, BandAdmin)
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Year, YearAdmin)

admin.site.register(Country)

admin.site.register(Profile)
admin.site.register(Comment)