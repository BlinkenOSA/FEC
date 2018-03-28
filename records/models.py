from django.db import models


class Corporation(models.Model):
    id = models.AutoField(primary_key=True)
    corporation = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.corporation

    def __unicode__(self):
        return self.corporation

    @staticmethod
    def autocomplete_search_fields():
        return ("corporation__icontains",)

    class Meta:
        db_table = 'fec_corporations'


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.country

    @staticmethod
    def autocomplete_search_fields():
        return ("country__icontains",)

    class Meta:
        db_table = 'fec_countries'


class FECEntity(models.Model):
    id = models.AutoField(primary_key=True)
    doc_name = models.CharField(max_length=100)
    title = models.CharField(max_length=150, blank=True)
    title_given = models.CharField(max_length=150, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    pages = models.IntegerField()
    is_coded = models.BooleanField(default=False)
    is_handwritten = models.BooleanField(default=False)
    summary = models.TextField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    internal_note = models.TextField(blank=True, null=True)
    confidential = models.BooleanField()

    place = models.ForeignKey('Place', default=1)

    associated_corporations = models.ManyToManyField('Corporation', related_name='associated_corporations', blank=True)

    countries = models.ManyToManyField('Country', blank=True)

    subject_people = models.ManyToManyField('Person', related_name='subject_people', blank=True)
    subject_corporations = models.ManyToManyField('Corporation', related_name='subject_corporations', blank=True)

    def __str__(self):
        return " - ".join(filter(None, (self.title, self.title_given)))

    def __unicode__(self):
        return " - ".join(filter(None, (self.title, self.title_given)))

    class Meta:
        db_table = 'fec_entities'
        verbose_name = 'FEC Entity'
        verbose_name_plural = 'FEC Entities'
        ordering = ('date', 'title')


class PersonRole(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return "%s" % self.role

    class Meta:
        db_table = 'fec_person_roles'


class AssociatedPerson(models.Model):
    id = models.AutoField(primary_key=True)
    fec_entity = models.ForeignKey('FECEntity', related_name='associated_people')
    person = models.ForeignKey('Person')
    role = models.ForeignKey('PersonRole', blank=True, null=True)

    class Meta:
        db_table = 'fec_associated_person'


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    person = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.person

    def __unicode__(self):
        return u'%s' % self.person

    @staticmethod
    def autocomplete_search_fields():
        return ("person__icontains",)

    class Meta:
        db_table = 'fec_people'


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    place = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.place

    class Meta:
        db_table = 'fec_places'
