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

class RecyclingComplaint(models.Model):
    created_date = models.DateField(name='created_date', verbose_name='Date complaint was created')
    closed_date = models.DateField(name='closed_date', verbose_name='Date complaint was closed')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='recycling_complaints')
    x_coord = models.DecimalField(max_digits=20, decimal_places=9)
    y_coord = models.DecimalField(max_digits=20, decimal_places=9)