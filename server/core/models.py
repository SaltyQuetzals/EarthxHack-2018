from django.db import models

# Create your models here.


class District(models.Model):
    number = models.IntegerField(primary_key=True)
    area = models.DecimalField(max_digits=40, decimal_places=30)
    population = models.IntegerField()

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
    created_date = models.DateField(
        name='created_date', verbose_name='Date complaint was created')
    closed_date = models.DateField(
        name='closed_date', verbose_name='Date complaint was closed')
    latitude = models.DecimalField(max_digits=20, decimal_places=9)
    longitude = models.DecimalField(max_digits=20, decimal_places=9)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='recycling_complaints')
    score = models.DecimalField(max_digits=20, decimal_places=10)


class GarbageComplaint(models.Model):
    created_date = models.DateField(
        name='created_date', verbose_name='Date complaint was created')
    closed_date = models.DateField(
        name='closed_date', verbose_name='Date complaint was closed')
    latitude = models.DecimalField(max_digits=20, decimal_places=9)
    longitude = models.DecimalField(max_digits=20, decimal_places=9)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name='garbage_complaints')
    score = models.DecimalField(max_digits=20, decimal_places=10)
