from django.db import models

# Create your models here.


class District(models.Model):
    number = models.IntegerField(primary_key=True)
    area = models.DecimalField(max_digits=40, decimal_places=30)

    class Meta:
        ordering = ('number',)



class CouncilMember(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=256, null=True)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='council_member')

    class Meta:
        ordering = ('name',)
