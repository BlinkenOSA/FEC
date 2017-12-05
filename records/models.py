from django.db import models


class Corporation(models.Model):
    id = models.AutoField(primary_key=True)
    corporation = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.corporation

    class Meta:
        db_table = 'fec_corporations'


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country

    class Meta:
        db_table = 'fec_countries'


class FECEntity(models.Model):
    id = models.AutoField(primary_key=True)
    doc_name = models.CharField(max_length=100)
    title = models.CharField(max_length=20, blank=True)
    title_given = models.CharField(max_length=100)
    date = models.DateField(blank=True, null=True)
    pages = models.IntegerField()
    is_coded = models.BooleanField(default=False)
    is_handwritten = models.BooleanField(default=False)
    summary = models.TextField(blank=True)
    note = models.CharField(max_length=200, blank=True)
    internal_note = models.CharField(max_length=200, blank=True)
    origin = models.CharField(max_length=20)
    confidential = models.BooleanField()

    def __str__(self):
        return " - ".join(filter(None, (self.title, self.title_given)))

    class Meta:
        db_table = 'fec_entities'


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.person

    class Meta:
        db_table = 'fec_people'


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.place

    class Meta:
        db_table = 'fec_places'
