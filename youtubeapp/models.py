from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from autoslug import AutoSlugField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=150)

class Youtuber(models.Model):
    youtuber = models.OneToOneField(User, on_delete=models.CASCADE)
    youtube_image = models.ImageField(upload_to='youtubeimage/')
    subscribers = models.ManyToManyField(User, blank=True, related_name='subs')
    channel_name = models.CharField(max_length=100)
    about = models.TextField()

    def image_tag(self):
        return format_html(f'<img src="/media/{self.youtube_image}" style="width:40px;height:40px;border-radius:50%;"  />')

class Video(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    video_thumbnail = models.ImageField(upload_to="thumbnails/")
    video_title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='video_title', unique=True, null=True)
    like = models.ManyToManyField(User, blank=True, related_name='like')
    dislike = models.ManyToManyField(User, blank=True, related_name='dislike')
    saved_post = models.ManyToManyField(User, blank=True, related_name='saved')
    video_desc = models.TextField()
    video = models.FileField(upload_to="youtubevideos/")
    add_date = models.DateTimeField(auto_now_add=True,null=True)

    def total_likes(self):
        return self.like.count()

    def image_tag(self):
        return format_html(f'<img src="/media/{self.video_thumbnail}" style="width:40px;height:40px;border-radius:50%;"  />')