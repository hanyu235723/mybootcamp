from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

class Messager(models.Model):
    User = settings.AUTH_USER_MODEL
    author = models.ForeignKey(User,related_name="message_author",on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()

    @classmethod
    def get_last_10_messages(cls):
        return Messager.objects.order_by('-create_date').all()[:10]

    def __str__(self):
        return self.author.email
