from django.urls import path
from youtubeapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addvideo/', views.add_video, name='addvideo'),
    path('search/',views.search_video, name='search'),
    path('userchannel/<slug:slug>',views.user_channel, name='userchannel'),
    path('subs<slug:slug>/',views.channel_subs, name='subs'),
    path('userprofile/',views.user_profile, name='userprofile'),
    path('updatevideo/<int:id>',views.video_update,name='updatevideo'),
    path('deletevideo/<int:id>',views.delete_video,name='deletevideo'),
    path('uservideos/',views.user_video, name='uservideos'),
    path('uliked/',views.user_liked, name='uliked'),

    path('video/<slug:slug>', views.video, name='video'),
    path('subscribe/<slug:slug>/',views.subscribe_channel, name='subscribe'),
    path('like<slug:slug>/',views.like_video, name='like'),
    path('dislike<slug:slug>/',views.dislike_video, name='dislike'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('signup/', views.user_signup, name='signup'),
    path('account-verify/<slug:token>', views.user_account_verify, name='account-verify'),

    path('password-change/', views.user_password_change, name='change-password'),
    path('password-reset/<slug:token>', views.user_password_reset, name='reset-password'),
    path('user-email-send/', views.user_email_send, name='send-email'),

] 
