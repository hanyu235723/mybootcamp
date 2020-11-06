from django.shortcuts import render,redirect
from django.views.generic.edit import FormMixin, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth import authenticate,login,get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import BaseBackend

from Accounts.models import Friend
from Accounts.forms import SignUpForm,myauthenticationForm

User = get_user_model()

class SettingsBackend(BaseBackend):
     
    def authenticate(self, request, email=None, password=None):
        user = User.objects.get(email=email)
        return user
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class Login (LoginView):
    template_name = "Accounts/Login.html"
    authentication_form = myauthenticationForm
    
def Index(request):
    #currentuser = User.objects.get(email=request.user.email)
    return render(request,'Accounts/Index.html')
 
def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request,'Chat/loginsuccessful.html')
           # return redirect(User)
        else:
            
            return render(request, 'Chat/SignUp.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'Chat/SignUp.html', {'form': form})


def UserProfile(request):
    return render(request,'Accounts/UserProfile.html')

 
@login_required 
def AddnewFriend(request):
    model = User
    template_name = 'Accounts/Addfriends.html'
    allUsers = User.objects.all()
    current_user = request.user
    friends_list = Friend.get_all_friends(current_user)
    if request.method == 'POST':
    # refer to django httprequest attributes ,would findout more about request.user information     
        friend = User.objects.get(email=request.POST.get('friend'))
        Friend.make_new_friends(user = current_user, friend=friend)
    return render(request,template_name,{'friends_list':friends_list,'allusers':allUsers})

class ContactView (LoginRequiredMixin,TemplateView):
    template_name = "Accounts/Contacts.html"
    
    def setup(self, request, *args, **kwargs):
        """Initialize attributes shared by all view methods."""
        if hasattr(self, 'get') and not hasattr(self, 'head'):
            self.head = self.get
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.current_user = self.request.user
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        allUsers = User.objects.all()
        friends_list = Friend.get_all_friends(self.current_user)
        context['friend_list'] = friends_list
        context['allusers'] = allUsers
        context['currentuser'] = self.current_user
       
        return context

    def post(self,request,**kwargs):
        friend = User.objects.get(email=request.POST.get('friend'))
        Friend.make_new_friends(user = self.current_user, friend=friend)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)