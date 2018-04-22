from django.db import models

# Create your models here.


class ProximityManager(models.Manager):
    def close_proximity(self, latitude, longitude):
        longitude, latitude = float(longitude), float(latitude)
        min_latitude = latitude - 0.030
        max_latitude = latitude + 0.030

        min_longitude = longitude - 0.0334
        max_longitude = longitude + 0.0334

        queryset = super(ProximityManager, self).get_queryset().filter(longitude__gte=min_longitude,
                                                                       longitude__lte=max_longitude, latitude__gte=min_latitude, latitude__lte=max_latitude)
        return queryset


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

    objects = ProximityManager()


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

    objects = ProximityManager()
