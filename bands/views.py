import datetime
import random
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Q
from django.db.models import Min, Max
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
# from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

import json

from urllib.request import urlopen

from .context_processors import *
from .models import *
from .forms import *

from decouple import config

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

from googleapiclient.discovery import build

from . import bandparse

with open('bands\countries.json') as json_file:
    countries_data = json.load(json_file)
flags = {}
for country in countries_data:
    flags[country['name']] = country['file_url']
        
objects_per_page = 60  # 60, because 60 is divisible by 5, 4, 3, 2, 1 (nice to )

ytapikey = config('YTAPIKEY')

def videosearch(title):
    youtube = build('youtube', 'v3', developerKey=ytapikey)
    search_response = youtube.search().list(
    q=title,
    type='video',
    part='id',
    maxResults=1
    ).execute()
    if search_response:
        video_id = search_response['items'][0]['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        return video_url
    return None

def createyears(min:int, max:int):
    if max > min:
        for year in range(max + 1 - min):
            Year.objects.get_or_create(number=min+year)
        
def createband(url, browser):
    band = bandparse.getbandsdata(url, browser)
    country = Country.objects.get_or_create(name=band['country'], flag=flags[band['country']])
    newband = Band.objects.get_or_create(
        
        name=band['name'],
        country=country[0],
        found_year=band['found_year'],
        breakup_year=band['breakup_year'],
        logo=band['logo'],
        bandphoto=band['band_photo'],
        genres=band['genre'],
        link=band['link']
        )
    newband[0].save()
    for album in band['albumslist']:
        year = Year.objects.get_or_create(number=album['album_year'])
        newalbum = Album.objects.get_or_create(
            
            name=album['album_name'],
            band=newband[0],
            release_year=year[0],
            cover=album['album_cover'],
            )
        newalbum[0].save()
        for song in album['songslist']:
            h = song['song_duration'][-8:-6]
            m = song['song_duration'][-5:-3]
            s = song['song_duration'][-2:]
            try:
                d = datetime.time(int(h) if h else 0, int(m) if m else 0, int(s))
            except:
                d = datetime.time(0,random.choice(range(3,6)),random.choice(range(60)))
            newsong = Song.objects.get_or_create(
                
            name=song['song_name'],
            album=newalbum[0],
            duration=d,
            num=song['song_num'],
            # video=videosearch(f"{band['name']} - {song['song_name']}"),
            )
            if newsong[0].name != '-' or '...':
                newsong[0].save()
    for member in band['memberslist']:
        newmember = Musician.objects.update_or_create(
            
        name=member['member_name'],
        profession=member['member_prof'],
        birth_date=member['member_age'],
        death_date=member['member_rip'],
        photo=member['member_photo'],
        )
        newmember[0].save()
        newband[0].members.add(newmember[0])
    for exmember in band['exmemberslist']:
        newexmember = Musician.objects.update_or_create(
            
        name=exmember['exmember_name'],
        profession=exmember['exmember_prof'],
        birth_date=exmember['exmember_age'],
        death_date=exmember['exmember_rip'],
        photo=exmember['exmember_photo'],
        )
        newexmember[0].save()
        newband[0].exmembers.add(newexmember[0])
    newband[0].save()

def createPaginator(request, objects):
    paginator = Paginator(objects, objects_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page

def delete_comment(request, id):
    next = request.POST.get('next', '/')
    comment = get_object_or_404(Comment, id=id)
    comment.delete()

    return HttpResponseRedirect(next)

def like_post(request, instance, id):
    obj = instance.objects.get(id=id)
    obj.likes.add(request.user)
    obj.save()
    
    return redirect(f'one{instance.__name__.lower()}', id=id)

def like_band(request, id):
    return like_post(request, Band, id)
def like_album(request, id):
    return like_post(request, Album, id)
def like_musician(request, id):
    return like_post(request, Musician, id)
def like_song(request, id):
    return like_post(request, Song, id)

def delete_like_model(request, instance, id):
    obj = instance.objects.get(id=id)
    obj.likes.remove(request.user)
    obj.save()

    return redirect(f'one{instance.__name__.lower()}', id=id)

def delete_like_band(request, id):
    return delete_like_model(request, Band, id)
def delete_like_album(request, id):
    return delete_like_model(request, Album, id)
def delete_like_musician(request, id):
    return delete_like_model(request, Musician, id)
def delete_like_song(request, id):
    return delete_like_model(request, Song, id)

def home(request):
    return render(request, 'home.html',
                  {

                  })

def onemodel(request, instance, id, *args): # One common function for representing all instanses
    try:
        obj = instance.objects.get(id=id)
        if request.method == 'POST':
            commentarea = request.POST.get('commentarea')
            if commentarea:
                Comment.objects.create(content_object=obj, text=commentarea, user=request.user)
            return redirect(f'one{instance.__name__.lower()}', id=id)
        context = {
            instance.__name__.lower(): obj,
            'comments': obj.comments if hasattr(obj, 'comments') else None,
            'like': obj.likes.filter(id=request.user.id) if hasattr(obj, 'likes') else None
            }
        try:
            
            context['like'] = obj.likes.get(user=request.user)
        except:
            pass
        for arg in args:
            context[f'{arg=}'] = arg
        return render(request, f'{instance.__name__.lower()}s/one{instance.__name__.lower()}.html', context)
    except ObjectDoesNotExist:
        return redirect('home')
    
def manymodels(request, instance):
    if instance != Country:
        objs = instance.objects.annotate(num_likes=Count('likes')).order_by('-num_likes', 'name')
    else:
        objs = instance.objects.all().order_by('name')
    return render(request, f'{instance.__name__.lower()}s/{instance.__name__.lower()}s.html',
                  {
                      'page': createPaginator(request, objs),
                  })

def bands(request):
    return manymodels(request, Band)

def oneband(request, id):
    return onemodel(request, Band, id)

def albums(request):
    return manymodels(request, Album)

def onealbum(request, id):
    return onemodel(request, Album, id)

def musicians(request):
    return manymodels(request, Musician)

def onemusician(request, id):
    return onemodel(request, Musician, id)

def songs(request):
    return manymodels(request, Song)

def onesong(request, id):
    song = Song.objects.get(id=id)
    song.video = videosearch(f'{song.album.band.name} - {song.name}')
    song.save()
    return onemodel(request, Song, id, song)

def countrys(request):
    return manymodels(request, Country)

def onecountry(request, id):
    return onemodel(request, Country, id)

def years(request, n=default_year):
    minyear = Year.objects.values('number').aggregate(Min('number'))['number__min']
    maxyear = Year.objects.values('number').aggregate(Max('number'))['number__max']
    createyears(minyear, maxyear+1)
    try:
        context = {
                'minyear':minyear,
                'maxyear':maxyear,
                'rangeval':n,
                'year': Year.objects.get(number=n)
        }
        if request.method == 'POST':
            rangeval = request.POST.get('range')
            context['rangeval'] = rangeval
            context['year'] = Year.objects.get(number=rangeval)
        return render(request, 'years/years.html', context)
    except:
        return HttpResponseNotFound('Page not found')
        

def search(request):
    if request.method == 'POST':
        q = request.POST['q'] if len(request.POST['q']) > 2 else ''
        qdata = {
            'bands': Band.objects.all().filter(name__contains=q),
            'albums': Album.objects.all().filter(name__contains=q),
            'musicians': Musician.objects.all().filter(name__contains=q),
            'songs': Song.objects.all().filter(name__contains=q)
        }
        return render(request, 'search.html', {
            'q': q,
            'qdata': qdata
        })
    else:
        return render(request, 'search.html', {})


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    return render(request, 'login.html', {

    })


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):

    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'register.html', {
        'form': form
    })


def userProfile(request, id):
    profile = Profile.objects.get(user=User.objects.get(id=id))
    return render(request, 'profile.html', {
        'profile': profile
    })
    
def addbands(request):
    bands = Band.objects.all().order_by('id')
    if request.method == 'POST':
        bandlinks = request.POST.get('bandlinks').split('\n')
        try:
            firefox_options = Options()
            browser = webdriver.Firefox(options=firefox_options)
            browser.set_window_size(600,400)
            for link in bandlinks:  
                createband(link, browser)
            browser.close()
        except:
            messages.error(request, 'An error occured during band(s) creation')
            browser.close()
    return render(request, 'addbands.html', {
        'bands': bands
    })