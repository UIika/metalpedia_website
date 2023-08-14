from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from embed_video.fields import EmbedVideoField
from PIL import Image


class Year(models.Model):
    number = models.IntegerField(unique=True)
    
    class Meta:
        ordering = ['number']
        
    def __str__(self) -> str:
        return str(self.number)
    
class Country(models.Model):
    name = models.CharField(max_length=100)
    flag = models.URLField(blank=True, null=True)
        
    def __str__(self) -> str:
        return self.name
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.text

class Band(models.Model):
    name = models.CharField(max_length=200)
    country = models.ForeignKey(Country, related_name='bands', on_delete=models.SET_NULL, blank=True, null=True)
    found_year = models.IntegerField(blank=True, null=True)
    breakup_year = models.IntegerField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    bandphoto = models.URLField(blank=True, null=True)
    genres = models.CharField(max_length=200)
    link = models.URLField()
    
    comments = GenericRelation(Comment, related_query_name='band')
    likes = models.ManyToManyField(User, related_name='bands', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ['name']
    
class Musician(models.Model):
    name = models.CharField(max_length=100)
    bands = models.ManyToManyField(Band, blank=True, related_name='members')
    exbands = models.ManyToManyField(Band, blank=True, related_name='exmembers')
    profession = models.CharField(max_length=150, blank=True)
    birth_date = models.CharField(max_length=100)
    death_date = models.CharField(max_length=100, blank=True, null=True)
    photo = models.URLField(blank=True, null=True)
    
    comments = GenericRelation(Comment, related_query_name='musician')
    likes = models.ManyToManyField(User, related_name='musicians', blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name
    
    
    

class Album(models.Model):
    name = models.CharField(max_length=150)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')
    release_year = models.ForeignKey(Year, on_delete=models.SET_NULL, related_name='albums', blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    
    comments = GenericRelation(Comment, related_query_name='album')
    likes = models.ManyToManyField(User, related_name='albums', blank=True, null=True)
    
    class Meta:
        ordering = ['release_year__number', 'name']
    
    def __str__(self) -> str:
        return self.name
    

class Song(models.Model):
    name = models.CharField(max_length=200)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, blank=True, null=True, related_name='songs')
    duration = models.TimeField()
    num = models.IntegerField()
    video = EmbedVideoField()
    
    comments = GenericRelation(Comment, related_query_name='song')
    likes = models.ManyToManyField(User, related_name='songs', blank=True, null=True)
    
    def __str__(self) -> str:
        return f'{self.name}  -  {self.album.band}  -  {self.album}'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    avatar = models.ImageField(
        default='avatar.jpg', # default avatar
        upload_to='profile_avatars' # dir to store the image
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            # create a thumbnail
            img.thumbnail(output_size)
            # overwrite the larger image
            img.save(self.avatar.path)
            
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
post_save.connect(create_profile, sender=User)
