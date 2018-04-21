from django.db import models

# Create your models here.


class Representative(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=256, null=True)

    class Meta:
        ordering = ('name',)
