from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'Chat'
urlpatterns = [
   
    path('<str:room_name>/', views.room, name='room'),
]
   
    
    
  
