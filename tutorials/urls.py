from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('albums/', views.index, name='index'),
    path('albums/api/', views.AlbumList.as_view(), name='listview'),
    path('albums/forms/', views.form, name='form'),
    path('albums/<int:number>/', views.details, name='details'),
    path('albums/<int:number>/update/', views.update, name='update'),
    path('albums/<int:number>/delete/', views.delete, name='delete'),
    path('albums/<int:number>/addtosongs/', views.addtosong, name='addtosong'),
    path('albums/<int:number>/<str:song>/deletesong/', views.deletesong, name='deletesong'),
    path('register/', views.register, name='register'),
    path('albums/logout/', views.exit, name='logout'),
    path('login/', views.comein, name='login'),
    path('albumview/', views.IndexView.as_view(), name='indexview'),
    path('albumview/<int:pk>/', views.DetailView.as_view(), name='detailview'),

]