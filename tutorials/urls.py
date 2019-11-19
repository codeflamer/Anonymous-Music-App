from django.urls import path,re_path
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetCompleteView,PasswordResetConfirmView

urlpatterns = [
    path('', views.home,name='home'),
    path('albums/', views.index, name='index'),
    path('albums/forms/', views.form, name='form'),
    path('albums/<int:number>/', views.details, name='details'),
    path('albums/<int:number>/update/', views.update, name='update'),
    path('albums/<int:number>/delete/', views.delete, name='delete'),
    path('albums/<int:number>/addtosongs/', views.addtosong, name='addtosong'),
    path('albums/<int:number>/<str:song>/deletesong/', views.deletesong, name='deletesong'),
    path('register/', views.register, name='register'),
    path('albums/logout/', views.exit, name='logout'),
    path('login/', views.comein, name='login'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('playlists/', views.my_playlists, name='playlist'),
    path('playlists/<str:playlistname>/', views.myplaylists_songs, name='playlistsongs'),
    path('createplaylist/', views.create_playlist, name='createplaylist'),
    path('addtoplaylist/<str:alpha>/<int:num>/<str:playlist>/', views.add_or_remove_from_playlist, name='addorremoveplaylist'),


    path('change-password/', views.change_password, name='change_password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset-password/done/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset-password/complete/',PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'^resetpassword/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]