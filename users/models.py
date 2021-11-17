from django.db import models

class User(models.Model):
    kakao      = models.CharField(max_length=100)
    email      = models.CharField(max_length=100, unique=True)
    size       = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'