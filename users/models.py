from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username