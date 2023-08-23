from django import forms
from .models import Profile

class AvatarChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)