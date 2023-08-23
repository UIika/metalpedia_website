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
    
    path('profiles/', profiles, name='profiles'),
    path('profiles/<int:id>/', oneprofile, name='oneprofile'),
    
    path('delete_comment/<int:id>/', delete_comment, name='delete_comment'),
    
    path('like/<str:instance>/<int:id>/', like,  name='like'), 
    path('delete_like/<str:instance>/<int:id>/', delete_like, name='delete_like'),
    
    path('change_avatar/<int:id>/', change_avatar, name='change_avatar'),
    
    path('addbands', addbands, name='addbands')
    
]