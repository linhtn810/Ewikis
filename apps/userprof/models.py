from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    website_blog = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=60, null=True, blank=True)
    about = models.TextField(null=True, blank=True)