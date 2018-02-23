import MySQLdb as mdb
import dj_database_url
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand, call_command

from records.models import FECEntity, Place, Person, Country, Corporation


class Command(BaseCommand):
    help = 'Migrate FEC Records.'

    def handle(self, *args, **options):
        db = dj_database_url.config(conn_max_age=600)

        call_command('loaddata', 'place')
        self.migrate_countries(db)
        self.migrate_corporations(db)
        self.migrate_people(db)
        self.migrate_fec_entity_records(db)

    def migrate_countries(self, db):
        con = mdb.connect(user=db['USER'], passwd=db['PASSWORD'], db=db['NAME'], charset='utf8')
        cur = con.cursor(mdb.cursors.DictCursor)

        sql = "SELECT * FROM legacy_countries"

        cur.execute(sql)
        rows = cur.fetchall()

        # Country.objects.all().delete()

        for row in rows:
            print("Adding country: %s" % row['Country'])
            country = Country.objects.get_or_create(
                country=row['Country']
            )[0]
            country.save()

    def migrate_corporations(self, db):
        con = mdb.connect(user=db['USER'], passwd=db['PASSWORD'], db=db['NAME'], charset='utf8')
        cur = con.cursor(mdb.cursors.DictCursor)

        sql = "SELECT * FROM legacy_corporations"

        cur.execute(sql)
        rows = cur.fetchall()

        # Corporation.objects.all().delete()

        for row in rows:
            print("Adding corporation: %s" % row['Corporation'])
            corporation = Corporation.objects.get_or_create(
                corporation=row['Corporation']
            )[0]
            corporation.save()

    def migrate_people(self, db):
        con = mdb.connect(user=db['USER'], passwd=db['PASSWORD'], db=db['NAME'], charset='utf8')
        cur = con.cursor(mdb.cursors.DictCursor)

        sql = "SELECT * FROM legacy_people"

        cur.execute(sql)
        rows = cur.fetchall()

        # Person.objects.all().delete()

        for row in rows:
            print("Adding person: %s" % row['Person'])
            person_record = row['Person'].strip().split(', ')

            person = Person.objects.get_or_create(
                person=person_record[0]
            )[0]
            person.save()

    def migrate_fec_entity_records(self, db):
        con = mdb.connect(user=db['USER'], passwd=db['PASSWORD'], db=db['NAME'], charset='utf8')
        cur = con.cursor(mdb.cursors.DictCursor)
        cur_sub = con.cursor(mdb.cursors.DictCursor)

        sql = "SELECT * FROM legacy_FECentity WHERE Title IS NOT NULL"

        cur.execute(sql)
        rows = cur.fetchall()

        # FECEntity.objects.all().delete()

        for row in rows:
            print("Adding document: %s" % row['DocName'])

            try:
                fec_entity = FECEntity.objects.get(doc_name=row['DocName'])
            except ObjectDoesNotExist:
                if row['AssociatedPlace'] == 'New York City':
                    place = Place.objects.get(place='New York')
                else:
                    place = Place.objects.get(place=row['AssociatedPlace'])
                fec_entity = FECEntity(
                    id=row['ID'],
                    doc_name=row['DocName'],
                    title=row['Title'],
                    title_given=row['TitleGiven'],
                    date="%s-%s-%s" % (row['DateYY'], row['DateMM'], row['DateDD']),
                    pages=row['Pages'],
                    is_coded=row['IsCoded'],
                    is_handwritten=row['IsHandWritten'],
                    summary=row['Summary'],
                    note=row['Note'],
                    internal_note=row['InternalNote'],
                    confidential=row['NotToPublish'],
                    place=place
                )
                fec_entity.save()

            # AssociatedPeople
            sql = """
                  SELECT
                  legacy_FECEntitiesAssociatedPeople.FECEntityID,
                  legacy_people.Person
                  FROM legacy_people
                  INNER JOIN legacy_FECEntitiesAssociatedPeople ON
                    legacy_FECEntitiesAssociatedPeople.PersonID = legacy_people.ID
                  WHERE FECEntityID = %s
                  """

            cur_sub.execute(sql, (row['ID'],))
            sub_rows = cur_sub.fetchall()

            for sub_row in sub_rows:
                person = Person.objects.filter(person=sub_row['Person'].strip().split(', ')[0]).first()
                fec_entity.associated_people.add(person)

            # AssociatedCorporations
            sql = """
                  SELECT
                  legacy_FECEntitiesAssociatedCorporations.FECEntityID,
                  legacy_corporations.Corporation
                  FROM legacy_corporations
                  INNER JOIN legacy_FECEntitiesAssociatedCorporations ON
                    legacy_FECEntitiesAssociatedCorporations.CorporationID = legacy_corporations.ID
                  WHERE FECEntityID = %s
                  """

            cur_sub.execute(sql, (row['ID'],))
            sub_rows = cur_sub.fetchall()

            for sub_row in sub_rows:
                corporation = Corporation.objects.filter(corporation=sub_row['Corporation']).first()
                fec_entity.associated_corporations.add(corporation)

            # SpatialCoverage
            sql = """
                  SELECT
                  legacy_FECEntitiesSpatialCoverage.FECEntityID,
                  legacy_countries.Country
                  FROM legacy_countries
                  INNER JOIN legacy_FECEntitiesSpatialCoverage ON
                    legacy_FECEntitiesSpatialCoverage.CountryID = legacy_countries.ID
                  WHERE FECEntityID = %s
                  """

            cur_sub.execute(sql, (row['ID'],))
            sub_rows = cur_sub.fetchall()

            for sub_row in sub_rows:
                country = Country.objects.filter(country=sub_row['Country']).first()
                fec_entity.countries.add(country)

            # SubjectPeople
            sql = """
                  SELECT
                  legacy_FECEntitiesSubjectPeople.FECEntityID,
                  legacy_people.Person
                  FROM legacy_people
                  INNER JOIN legacy_FECEntitiesSubjectPeople ON
                    legacy_FECEntitiesSubjectPeople.PersonID = legacy_people.ID
                  WHERE FECEntityID = %s
                  """

            cur_sub.execute(sql, (row['ID'],))
            sub_rows = cur_sub.fetchall()

            for sub_row in sub_rows:
                person = Person.objects.filter(person=sub_row['Person'].strip().split(', ')[0]).first()
                fec_entity.subject_people.add(person)

            # SubjectCorporations
            sql = """
                  SELECT
                  legacy_FECEntitiesSubjectCorporations.FECEntityID,
                  legacy_corporations.Corporation
                  FROM legacy_corporations
                  INNER JOIN legacy_FECEntitiesSubjectCorporations ON
                    legacy_FECEntitiesSubjectCorporations.CorporationID = legacy_corporations.ID
                  WHERE FECEntityID = %s
                  """

            cur_sub.execute(sql, (row['ID'],))
            sub_rows = cur_sub.fetchall()

            for sub_row in sub_rows:
                corporation = Corporation.objects.filter(corporation=sub_row['Corporation']).first()
                fec_entity.subject_corporations.add(corporation)