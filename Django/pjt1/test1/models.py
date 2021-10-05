from django.db import models

#========================================================================
#========================================================================
#========================================================================
#========================================================================
#========================================================================

class Care(models.Model):
    id = models.IntegerField(primary_key=True)
    sigungu = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    post = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'care'


class ClusterData(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    land_number = models.IntegerField(blank=True, null=True)
    square_m = models.IntegerField(blank=True, null=True)
    wait_people = models.FloatField(blank=True, null=True)
    supply_type = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    fire_d = models.FloatField(blank=True, null=True)
    station_d = models.FloatField(blank=True, null=True)
    post_d = models.FloatField(blank=True, null=True)
    subway_d = models.FloatField(blank=True, null=True)
    department_d = models.FloatField(blank=True, null=True)
    police_d = models.FloatField(blank=True, null=True)
    traditional_d = models.FloatField(blank=True, null=True)
    convenience_d = models.FloatField(blank=True, null=True)
    high_d = models.FloatField(blank=True, null=True)
    kinder_d = models.FloatField(blank=True, null=True)
    middle_d = models.FloatField(blank=True, null=True)
    care_d = models.FloatField(blank=True, null=True)
    bus_d = models.FloatField(blank=True, null=True)
    hospital_d = models.FloatField(blank=True, null=True)
    cluster = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster_data'

class Pharmacy(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    sigungu = models.CharField(max_length=20, blank=True, null=True)
    postal = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    openday = models.DateField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pharmacy'

