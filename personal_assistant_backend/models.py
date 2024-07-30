from django.db import models

# Create your models here.

import uuid

class Chat(models.Model):
    # user_id = models.IntegerField()  # Assuming user_id is an integer. Adjust as needed.
    email = models.TextField()  # Adding email field
    guid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Adding guid field
    user_input = models.TextField()
    ai_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class User(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.first_name
