from django.contrib import admin
from youtubeapp.models import Profile, Youtuber, Video

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','token')
    search_fields = ('user',)

class YoutuberAdmin(admin.ModelAdmin):
    list_display = ('image_tag','youtuber',)
    search_fields = ('youtuber',)

class VideoAdmin(admin.ModelAdmin):
    list_display = ('image_tag','creator','slug','video_title')
    search_fields = ('video_title',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Youtuber, YoutuberAdmin)
admin.site.register(Video, VideoAdmin)