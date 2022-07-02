from django.shortcuts import render, redirect

from youtubeapp.models import Profile, Video, Youtuber

from django.contrib.auth import authenticate,login, logout, update_session_auth_hash

from youtubeapp.forms import SignUpForm, LoginForm, UserPasswordChange, UserPasswordReset, VideoForm, YoutuberForm

from django.contrib import messages

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
import uuid

from random import sample


from django.urls import reverse
from django.http import HttpResponseRedirect

def home(request):  

    youtube = Youtuber.objects.all()

    # for random videos
    p = list(Video.objects.all())
    l = len(p)
    video = sample(p, l)

    data = {
        'video':video,
        'youtube':youtube
    }
    return render(request, 'home.html', data)

def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = request.user.youtuber
            fm = YoutuberForm(request.POST,request.FILES,instance=id)
            if fm.is_valid():
                form = fm.save(commit=False)
                form.creator = request.user
                form.save()
                return render(request, 'userprofile.html', {'form':fm})
            
            else:
                return render(request, 'userprofile.html', {'form':fm})
        else:
            id = request.user.youtuber
            fm = YoutuberForm(instance=id)
            return render(request, 'userprofile.html', {'form':fm})
    else:
        return redirect('login')

def delete_video(request,id):
    id = Video.objects.get(pk=id)
    id.delete()
    return redirect('uservideos')

def video_update(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            id = Video.objects.get(pk=id)
            fm = VideoForm(request.POST,request.FILES,instance=id)
            if fm.is_valid():
                form = fm.save(commit=False)
                form.creator = request.user
                form.save()
                return redirect('uservideos')
            
            else:
                return render(request, 'addvideo.html', {'form':fm})
        else:
            id = Video.objects.get(pk=id)
            fm = VideoForm(instance=id)
            return render(request, 'addvideo.html', {'form':fm})
    else:
        return redirect('login')

def user_video(request):
    if request.user.is_authenticated:
        youtube = Youtuber.objects.all()

        video = Video.objects.filter(creator=request.user)

        data = {
            'video':video,
            'youtube':youtube
        }

        return render(request, 'uservideos.html', data)
    else:
        return redirect('login')

def user_liked(request):
    if request.user.is_authenticated:
        youtube = Youtuber.objects.all()

        user = request.user
        fav = user.like.all()
        
        data = {
            'video':fav,
            'youtube':youtube
        }

        return render(request, 'uservideos.html', data)
    else:
        return redirect('login')


def user_channel(request, slug):
    video = Video.objects.get(slug=slug)

    creator = video.creator
    creator_videos = Video.objects.filter(creator=creator)

    youtube = Youtuber.objects.get(youtuber=creator)
    subs = youtube.subscribers.count()

    youtuber_image = Youtuber.objects.all()

    subscribed = False
    if youtube.subscribers.filter(id=request.user.id).exists():
        subscribed = True

    data = {
        'video':video,
        'youtuber':youtuber_image,
        'youtube':youtube,
        'videos':creator_videos,
        'subs':subs,
        'subscribes':subscribed
    }

    return render(request, 'userchannel.html', data)

def channel_subs(request, slug):
    if request.user.is_authenticated:
        v = Video.objects.get(slug=slug)
        subs = Youtuber.objects.get(youtuber=v.creator)

        if subs.subscribers.filter(id=request.user.id).exists():
            subs.subscribers.remove(request.user)
        else:
            subs.subscribers.add(request.user)

        return HttpResponseRedirect(reverse('userchannel', args=[str(slug)]))
    else:
        return redirect('login')

def add_video(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = VideoForm(request.POST,request.FILES)
            if fm.is_valid():
                form = fm.save(commit=False)
                form.creator = request.user
                form.save()
                return redirect('uservideos')
            
            else:
                return render(request, 'addvideo.html', {'form':fm})
        else:
            fm = VideoForm()
            return render(request, 'addvideo.html', {'form':fm})
    else:
        return redirect('login')

def video(request, slug):
    video = Video.objects.get(slug=slug)

    likes = video.like.count()
    liked = False
    if video.like.filter(id=request.user.id).exists():
        liked = True

    dislike = video.dislike.count()
    disliked = False
    if video.dislike.filter(id=request.user.id).exists():
        disliked = True

    creator = video.creator
    youtube = Youtuber.objects.get(youtuber=creator)
    subs = youtube.subscribers.count()

    subscribed = False
    if youtube.subscribers.filter(id=request.user.id).exists():
        subscribed = True

    print(subscribed)
    youtubers = Youtuber.objects.all()

    # for random videos
    p = list(Video.objects.all())
    l = len(p)
    videos = sample(p, l)

    data = {
        'video':video,
        'likes':likes,
        'liked':liked,
        'dislike':dislike,
        'disliked':disliked,

        'subs':subs,
        'youtube':youtube,
        'subscribed':subscribed,

        'videos':videos,
        'youtubers':youtubers
    }

    return render(request, 'video.html', data)


def search_video(request):
    query = request.GET['query']
    video = Video.objects.filter(video_title__icontains=query)
    youtuber = Youtuber.objects.all()
    return render(request,'search.html',{'video':video, 'youtube':youtuber})

def subscribe_channel(request, slug):
    if request.user.is_authenticated:
        v = Video.objects.get(slug=slug)
        subs = Youtuber.objects.get(youtuber=v.creator)

        if subs.subscribers.filter(id=request.user.id).exists():
            subs.subscribers.remove(request.user)
        else:
            subs.subscribers.add(request.user)

        return HttpResponseRedirect(reverse('video', args=[str(slug)]))
    else:
        return redirect('login')

def like_video(request, slug):
    if request.user.is_authenticated:
        v = Video.objects.get(slug=slug)

        if v.like.filter(id=request.user.id).exists():
            v.like.remove(request.user)
        else:
            v.like.add(request.user)
            if v.dislike.filter(id=request.user.id).exists():
                v.dislike.remove(request.user)

        return HttpResponseRedirect(reverse('video', args=[str(slug)]))
    else:
        return redirect('login')

def dislike_video(request, slug):
    if request.user.is_authenticated:
        v = Video.objects.get(slug=slug)

        if v.dislike.filter(id=request.user.id).exists():
            v.dislike.remove(request.user)
        else:
            v.dislike.add(request.user)
            if v.like.filter(id=request.user.id).exists():
                v.like.remove(request.user)

        return HttpResponseRedirect(reverse('video', args=[str(slug)]))
    else:
        return redirect('login')

    

# ---------------login-----------------

def user_login(request):
    if not request.user.is_authenticated:
        if request.method=='POST':
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upassword = fm.cleaned_data['password']
                user = authenticate(username=uname,password=upassword)
                login(request, user)
                messages.success(request,'User Login Successfully !')
                return redirect('home')
            else:
                return render(request, 'login.html', {'form':fm})
        else:
            fm = LoginForm()
            return render(request, 'login.html', {'form':fm})
    else:
        return redirect('home')

def user_logout(request):
    logout(request)
    messages.success(request,'User Logout Successfully !')
    return redirect('home')

# ---------------------------------Signup---------------------------------------------

def email_verification(host ,email, token):
    subject = "Verify Email"
    message = f"Hi check your link http://{host}/account-verify/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_account_verify(request, token):
    pro_obj = Profile.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)

    if user.is_active == False:
        user.is_active = True
        user.save()
        return render(request, 'email-verification/send_email_verified.html')
    else:
        return render(request, 'email-verification/send_email_already_verified.html')

def user_signup(request):  
    if not request.user.is_authenticated:
        if request.method == 'POST':  
            form = SignUpForm(request.POST)  
            if form.is_valid():  
                user = form.save(commit=False)  
                user.is_active = False  
                user.save()  
                
                uid = uuid.uuid4()
                
                pro_obj = Profile(user=user, token=uid)
                youtuber_obj = Youtuber(youtuber=user)
                pro_obj.save()
                youtuber_obj.save()
                
                host = request.get_host()
                email_verification(host, user.email, uid)

                return render(request, 'email-verification/send_email_done.html')
            else:
                return render(request, 'signup.html', {'form': form}) 
        else:  
            form = SignUpForm()  
            return render(request, 'signup.html', {'form': form}) 
    else:
        return redirect('home')

# ----------------------------passwordreset-------------------------------------

def email_password_reset(host, email, token):
    subject = "Password Reset Link"
    message = f"Hi check your link http://{host}/password-reset/{token}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)

def user_password_change(request):
    if request.user.is_authenticated:
    
        if request.method == 'POST':  
            form = UserPasswordChange(user=request.user, data=request.POST) 
            if form.is_valid():  
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request,'Password changed Successfully !')
                return redirect('dashboard')
            else:
                return render(request, 'password-change/change_password.html', {'form': form})
        else:
            form = UserPasswordChange(user=request.user) 
            return render(request, 'password-change/change_password.html', {'form': form})
    else:
        return redirect('home')

def user_email_send(request):
    if request.method == 'POST':  
        email = request.POST['email']

        try:
            user = User.objects.get(email=email)
            pro_obj = Profile.objects.get(user=user)
            host = request.get_host()
            email_password_reset(host, email, pro_obj.token)
        except User.DoesNotExist or Profile.DoesNotExist:
            messages.warning(request,'Invalid Email !')
            return render(request, 'password-change/password_reset_email.html')

        return render(request, 'password-change/password_reset_email_done.html')
    else:
        return render(request, 'password-change/password_reset_email.html')

def user_password_reset(request, token):
    pro_obj = Profile.objects.get(token=token)
    user = User.objects.get(username=pro_obj.user)

    if request.method == 'POST':  
        form = UserPasswordReset(user=user, data=request.POST) 
        if form.is_valid():  
            form.save()
            return render(request, 'password-change/password_reset_done.html')
        else:
            return render(request, 'password-change/password_reset.html', {'form': form})
    else:
        form = UserPasswordReset(user=user) 
        return render(request, 'password-change/password_reset.html', {'form': form})

# ---------------------------------------------------------------------