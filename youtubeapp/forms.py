import imp
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserChangeForm
from youtubeapp.models import Youtuber, Video

class UserPasswordReset(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

class UserPasswordChange(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x1','placeholder':'Password'}), label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='New Password Confirmation')

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}),min_length=4, max_length=10)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control x1','placeholder':'Email'}))  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x2','placeholder':'Password'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control x3','placeholder':'Confirm password'}), label='Password Confirmation')

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x5','placeholder':'last name'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            msg = 'A user with that email already exists.'
            self.add_error('email', msg)           
    
        return self.cleaned_data

class UserEditForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control x1','placeholder':'Username'}),min_length=4, max_length=10)  
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control x1','placeholder':'Email'}))  
    password = None

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'email':'Email'}
        widgets = {
            'first_name':forms.TextInput(attrs={'class':'form-control x4','placeholder':'first name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control x5','placeholder':'last name'}),
        }
    
class YoutuberForm(forms.ModelForm):
    class Meta:
        model = Youtuber
        fields = ['youtube_image','channel_name','about']
        labels = {'youtube_image':'Upload Image','channel_name':'Channel Name','about':'About'}
        widgets = {
            'youtube_image':forms.FileInput(attrs={'class':'form-control'}),
            'channel_name':forms.TextInput(attrs={'class':'form-control'}),
            'about':forms.TextInput(attrs={'class':'form-control','placeholder':'Content'})
        }

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video_thumbnail','video_title','video_desc','video']
        labels = {'video_thumbnail':'video_thumbnail','video_title':'video_title','video_desc':'video_desc','video':'video'}
        widgets = {
            'video_thumbnail':forms.FileInput(attrs={'class':'form-control'}),
            'video_title':forms.TextInput(attrs={'class':'form-control'}),
            'video_desc':forms.TextInput(attrs={'class':'form-control'}),
            'video':forms.FileInput(attrs={'class':'form-control'})
        }
