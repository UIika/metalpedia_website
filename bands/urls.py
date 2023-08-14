from django.urls import path

from bands.views import *

urlpatterns = [
    path('', home, name='home'),
    
    path('bands/', bands, name='bands'),
    path('bands/<int:id>/', oneband, name='oneband'),
    
    path('albums/', albums, name='albums'),
    path('albums/<int:id>/', onealbum, name='onealbum'),
    
    path('musicians/', musicians, name='musicians'),
    path('musicians/<int:id>/', onemusician, name='onemusician'),
    
    path('songs/', songs, name='songs'),
    path('songs/<int:id>/', onesong, name='onesong'),
    
    path('years/<int:n>/', years, name='years'),
    
    path('countries/', countrys, name='countries'),
    path('countries/<int:id>/', onecountry, name='onecountry'),
    
    path('search/', search, name='search'),
    
    path('login/', loginPage, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('register/', registerPage, name='register'),
    
    path('profile/<int:id>/', userProfile, name='profile'),
    
    path('delete_comment/<int:id>/', delete_comment, name='delete_comment'),
    
    path('like_band/<int:id>/', like_band,  name='like_band'),
    path('like_album/<int:id>/', like_album,  name='like_album'),
    path('like_musician/<int:id>/', like_musician,  name='like_musician'),
    path('like_song/<int:id>/', like_song,  name='like_song'),
    
    path('delete_like_band/<int:id>/', delete_like_band, name='delete_like_band'),
    path('delete_like_album/<int:id>/', delete_like_album, name='delete_like_album'),
    path('delete_like_musician/<int:id>/', delete_like_musician, name='delete_like_musician'),
    path('delete_like_song/<int:id>/', delete_like_song, name='delete_like_song'),
    
    path('addbands', addbands, name='addbands')
    
]