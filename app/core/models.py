import uuid
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis import geos

from geopy.exc import GeocoderTimedOut
from geopy.geocoders import GoogleV3
from urllib.request import URLError

geocoder = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)

def pipl_image_file_path(instance, filename):
    """generate filepath for new pipl image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/pipl/', filename)


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, email, password=None):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tags to be tied to pips"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    location = models.PointField(geography=True, default=Point(0.0, 0.0))
    
    def __str__(self):
        return self.name


class Reminder(models.Model):
    """Reminders to be tied to pips"""
    title = models.CharField(max_length=255)
    date = models.DateField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    pip = models.ForeignKey('Pip', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Pip(models.Model):

    CATEGORY_OPTIONS = [
        ('FAMILY', 'FAMILY'),
        ('FRIEND', 'FRIEND'),
        ('COLLEAGUE', 'COLLEAGUE'),
        ('ACQUAINTANCE', 'ACQUAINTANCE'),
        ('POI', 'POI')
    ]

    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=255)
    name = models.CharField(max_length=255)
    date_met = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    location = models.PointField(geography=True, blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    phone = models.CharField(max_length=255, blank=True)
    image = models.ImageField(null=True, upload_to=pipl_image_file_path)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.location and self.address:
            user_address = self.address
            try:
                user_location = geocoder.geocode(user_address, timeout=10)
            except(URLError, ValueError, TypeError, GeocoderTimedOut) as e:
                print("Error: geocode failed on input %s with message %s"%(user_address, e.message))
                pass
            if user_location:
                longitude = user_location.longitude
                latitude = user_location.latitude
                point = "POINT(%s %s)" % (longitude, latitude)
                self.location = geos.fromstr(point)
            else:
                print('Could not GEOCODE address')
                print(self.location)
        super(Pip, self).save(*args, **kwargs)


class Note(models.Model):
    """Note to be tied to pips"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="notes_owner",blank=True,null=True, on_delete=models.CASCADE)
    pip = models.ForeignKey('Pip', related_name="pip_notes", on_delete=models.SET_NULL, null=True)
    pinned = models.BooleanField(default=False)
    note_title = models.CharField(max_length=400)
    note_content = models.TextField(max_length=20000, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note_title
