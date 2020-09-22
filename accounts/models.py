from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class CustomUser(AbstractUser):
    """ A class to manage site users """
    age = models.PositiveIntegerField(default=0)
    occupation = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class Profile(models.Model):
    """ A class to manage user profiles """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"

#    def save(self, *args, **kwargs):
#        super().save(*args, **kwargs)
#
#        img = Image.open(self.image.path)
#        # Crop Large images
#        if img.height > 300 or img.width > 300:
#            output_size = (300, 300)
#            img.thumbnail(output_size)
#            img.save(self.image.path)
#
