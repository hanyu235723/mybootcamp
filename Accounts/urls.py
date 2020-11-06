from django.urls import path
from . import views

app_name = 'Accounts'
urlpatterns = [
    path('/', views.Index,name = 'index'),
    path('login/',views.Login.as_view(),name='logIn'),
    path('signUp/',views.SignUp,name='signup'),
    path('profile/',views.UserProfile,name='userprofile'),
    path('contacts/',views.ContactView.as_view(),name='contacts'),

]
