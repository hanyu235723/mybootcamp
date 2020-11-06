from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from django.contrib.auth.hashers import check_password


class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, first_name,last_name,password=None):
        if not email:
            raise ValueError(_('The Email must be set'))

        user = self.model(email=self.normalize_email(email),first_name = first_name,last_name = last_name,
                          date_of_birth=date_of_birth)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,
                         email,
                         date_of_birth,
                         first_name,
                         last_name,
                         password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        Superuser = self.create_user(email,
                                     password=password,
                                     first_name = first_name,
                                     last_name= last_name,
                                     date_of_birth=date_of_birth)
        Superuser.is_staff = extra_fields.get('is_staff')
        Superuser.is_superuser = extra_fields.get('is_superuser')
        Superuser.is_admin = extra_fields.get('is_admin')

        Superuser.save()
        return Superuser


class User(AbstractUser):
    username = None
    email = models.EmailField(
        'Email Address',
        unique=True,
        error_messages={
            'unique': ("A user with that email already exists."),
            'required': ('please fill in the email address'),
        },
    )
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']

    objects = CustomUserManager()

    class Meta:
        app_label = 'Accounts'
        db_table = 'auth_user'

    def __str__(self):
        return self.email


class Friend(models.Model):
    current_user = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE,related_name="owner")
    friends = models.ManyToManyField(User)

    @classmethod
    def get_all_friends(cls, user: User):
        all_friends = list()
        try:
            owner_friend_list =  cls.objects.get(current_user=user).friends.all() 
            user_friend_list = user.friend_set.all()
            for friend in user_friend_list:
                all_friends.append(friend)
            for owner in owner_friend_list:
                all_friends.append(owner)
           
            return all_friends
            
        except ObjectDoesNotExist:
            try :
                user_friend_list = user.friend_set.all()
                for friend in user_friend_list:
                    all_friends.append(friend)
                return all_friends
                        
            except ObjectDoesNotExist:
                return None

            
    @classmethod
    def make_new_friends(cls, user:User, friend:User):
        owner, created = cls.objects.get_or_create(current_user=user)
        
        owner.friends.add(friend)
      

    def remove_friend(cls, user:User, friend:User):
        
        cls.objects.get(current_user=user).friends.remove(friend)

    def __str__(self):
        return self.current_user.__str__()
