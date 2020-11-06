



def populate_users():
   
    user = User.objects.create_superuser(
        'superuser@gmail.com', '2001-01-01','superfname','superlname','1234test')
    user.save()
    user = User.objects.create_user(
        'testuser1@gmail.com', '2001-01-01','user1fname','user1lname','1234test')
    user.save()
    user = User.objects.create_user(
        'testuser2@gmail.com', '2001-01-01','user2fname','user2lname','1234test')
    user.save()
    user = User.objects.create_user(
        'testuser3@gmail.com', '2001-01-01','user3fname','user3lname','1234test')
    user.save()
    user = User.objects.create_user(
        'testuser4@gmail.com', '2001-01-01','user4fname','user4lname','1234test')
    user.save()


if __name__ == '__main__':
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mybootcamp.settings")
    django.setup()
    from django.contrib.auth import get_user_model
    from Accounts.models import User
    import django
    
    populate_users()