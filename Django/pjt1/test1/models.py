from django.db import models

#========================================================================
#========================================================================
#========================================================================
#========================================================================
#========================================================================
class Blog(models.Model):
    title = models.CharField(max_length=50, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    pwd = models.IntegerField(blank=True, null=True)
    writer = models.CharField(max_length=20, blank=True, null=True)
    hit = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'Blog'

class Commet(models.Model):
    body = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateField()
    blog = models.ForeignKey(Blog, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'commet'

class NoticeBlog(models.Model):
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=100)
    name = models.CharField(max_length=10)
    date = models.DateField(blank=True, null=True)
    hit = models.IntegerField(blank=True, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'notice_blog'
       

class Bus(models.Model):
    id = models.IntegerField(primary_key=True)
    ars_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True)
    latitude = models.DecimalField(max_digits=13, decimal_places=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bus'


class Care(models.Model):
    id = models.IntegerField(primary_key=True)
    sigungu = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=60, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)
    post = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'care'


class ClusterData(models.Model):
    id = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    land_name = models.CharField(max_length=30, blank=True, null=True)
    square_m = models.IntegerField(blank=True, null=True)
    wait_people = models.FloatField(blank=True, null=True)
    supply_type = models.CharField(max_length=16, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    fire_d = models.FloatField(blank=True, null=True)
    station_d = models.FloatField(blank=True, null=True)
    elementary_d = models.FloatField(blank=True, null=True)
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


class Convenience(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    station_id = models.IntegerField(blank=True, null=True)
    large_category = models.CharField(max_length=6, blank=True, null=True)
    middle_category = models.CharField(max_length=12, blank=True, null=True)
    small_category = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'convenience'


class Depart(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField(blank=True, null=True)
    large_category = models.CharField(max_length=4, blank=True, null=True)
    medium_category = models.CharField(max_length=10, blank=True, null=True)
    small_category = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'depart'


class Fire(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fire'


class Hospital(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=80, blank=True, null=True)
    type_code = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    si_code = models.IntegerField(blank=True, null=True)
    si = models.CharField(max_length=4, blank=True, null=True)
    gu_code = models.IntegerField(blank=True, null=True)
    gu = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    openday = models.DateField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hospital'


class Kinder(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    edu_name = models.CharField(max_length=24, blank=True, null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=14, blank=True, null=True)
    establish_date = models.DateField(blank=True, null=True)
    openday = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'kinder'


class Parking(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    station_code = models.IntegerField(blank=True, null=True)
    large_category = models.CharField(max_length=10, blank=True, null=True)
    middle_category = models.CharField(max_length=20, blank=True, null=True)
    small_category = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parking'


class Pharmacy(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    sigungu = models.CharField(max_length=10, blank=True, null=True)
    postal = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    openday = models.DateField(blank=True, null=True)
    longitude = models.TextField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pharmacy'


class Police(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    agency = models.CharField(max_length=20, blank=True, null=True)
    station = models.CharField(max_length=20, blank=True, null=True)
    police_station = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'police'


class Post(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    station_code = models.IntegerField(blank=True, null=True)
    large_category = models.CharField(max_length=10, blank=True, null=True)
    middle_category = models.CharField(max_length=20, blank=True, null=True)
    small_category = models.CharField(max_length=22, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'



class School(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    school_id = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=40, blank=True, null=True)
    classification = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'

class Seoul(models.Model):
    id = models.IntegerField(primary_key=True)
    entrepreneur = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=80, blank=True, null=True)
    address_gu = models.CharField(max_length=20, blank=True, null=True)
    land_name = models.CharField(max_length=40, blank=True, null=True)
    household = models.SmallIntegerField(blank=True, null=True)
    housing_type = models.CharField(max_length=10, blank=True, null=True)
    supply_type = models.CharField(max_length=16, blank=True, null=True)
    wait_people = models.TextField(blank=True, null=True)
    square_m = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seoul'

        
class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_id = models.IntegerField(blank=True, null=True)
    large_category = models.CharField(max_length=20, blank=True, null=True)
    middle_category = models.CharField(max_length=30, blank=True, null=True)
    small_category = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store'


class Subway(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    station_num = models.SmallIntegerField(blank=True, null=True)
    line_num = models.IntegerField(blank=True, null=True)
    station_nam = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subway'

