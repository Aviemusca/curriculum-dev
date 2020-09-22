from django.db import models


class Contact(models.Model):
    """ A class to manage contact messages """
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=250)
    message = models.TextField(default='')

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        return self.message


