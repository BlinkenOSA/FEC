import mysql.connector
import dj_database_url
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.management import BaseCommand, call_command
from django.db import IntegrityError

from records.models import FECEntity, Place, Person, Country, Corporation, AssociatedPerson


class Command(BaseCommand):
    help = 'Migrate FEC Records.'

    def handle(self, *args, **options):
        db = dj_database_url.config(conn_max_age=600)

        call_command('loaddata', 'place')
        self.clean_records(db)
        self.migrate_countries(db)
        self.migrate_corporations(db)
        self.migrate_people(db)
        self.migrate_fec_entity_records(db)

    def clean_records(self, db):
        con = mysql.connector.connect(user=db['USER'], host=db['HOST'], password=db['PASSWORD'], database=db['NAME'])
        cursor = con.cursor()

        sql = "DELETE FROM legacy_FECEntity WHERE legacy_FECEntity.InternalNote LIKE '%Competely illegible%' OR " \
              "legacy_FECEntity.InternalNote LIKE '%Competly illegible%' OR " \
              "legacy_FECEntity.InternalNote LIKE '%Completely illegible%' OR " \
              "legacy_FECEntity.InternalNote LIKE '%Completly illegible%'"
        cursor.execute(sql)
        con.commit()

        sql = "UPDATE legacy_FECEntity SET legacy_FECEntity.AssociatedPlace = 'New York' " \
              "WHERE legacy_FECEntity.Title LIKE '%NYC%' OR legacy_FECEntity.Title LIKE '%NCY%' OR " \
              "legacy_FECEntity.Title LIKE '%NY%'"
        cursor.execute(sql)
        con.commit()

        sql = "UPDATE legacy_FECEntity SET legacy_FECEntity.AssociatedPlace = 'Lisbon' " \
              "WHERE legacy_FECEntity.Title LIKE '%LIS%'"
        cursor.execute(sql)
        con.commit()

        sql = "UPDATE legacy_FECEntity SET legacy_FECEntity.AssociatedPlace = 'Munich' " \
              "WHERE legacy_FECEntity.Title LIKE '%MUN%' OR legacy_FECEntity.Title LIKE '%MU%' " \
              "OR legacy_FECEntity.Title LIKE '%MUF%'"
        cursor.execute(sql)
        con.commit()

        cursor.close()
        con.close()

    def migrate_countries(self, db):
        con = mysql.connector.connect(user=db['USER'], host=db['HOST'], password=db['PASSWORD'], database=db['NAME'])
        cur = con.cursor(dictionary=True)

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
        con = mysql.connector.connect(user=db['USER'], host=db['HOST'], password=db['PASSWORD'], database=db['NAME'])
        cur = con.cursor(dictionary=True)

        sql = "SELECT * FROM legacy_corporations"

        cur.execute(sql)
        rows = cur.fetchall()

        # Corporation.objects.all().delete()

        for row in rows:
            print("Adding corporation: %s" % row['Corporation'].encode('utf-8'))
            corporation = Corporation.objects.get_or_create(
                corporation=row['Corporation']
            )[0]
            corporation.save()

    def migrate_people(self, db):
        con = mysql.connector.connect(user=db['USER'], host=db['HOST'], password=db['PASSWORD'], database=db['NAME'])
        cur = con.cursor(dictionary=True)

        sql = "SELECT * FROM legacy_people"

        cur.execute(sql)
        rows = cur.fetchall()

        # Person.objects.all().delete()

        for row in rows:
            print("Adding person: %s" % row['Person'].encode('utf-8'))
            person_record = row['Person'].strip().split(', ')

            person = Person.objects.get_or_create(
                person=person_record[0]
            )[0]
            person.save()

    def migrate_fec_entity_records(self, db):
        skip = False
        con = mysql.connector.connect(user=db['USER'], host=db['HOST'], password=db['PASSWORD'], database=db['NAME'])
        cur = con.cursor(dictionary=True)
        cur_sub = con.cursor(dictionary=True)

        sql = "SELECT * FROM legacy_FECEntity WHERE " \
              "Title IS NOT NULL AND AssociatedPlace IS NOT NULL AND DateDD IS NOT NULL " \
              "ORDER BY DocName"

        cur.execute(sql)
        rows = cur.fetchall()

        # FECEntity.objects.all().delete()
        AssociatedPerson.objects.all().delete()

        for row in rows:
            print("Adding document: %s" % row['DocName'])

            fec_entity, created = FECEntity.objects.get_or_create(doc_name=row['DocName'])
            if row['AssociatedPlace'] == 'New York City':
                place = Place.objects.get(place='New York')
            else:
                place = Place.objects.get(place=row['AssociatedPlace'])

            fec_entity.id = row['ID']
            fec_entity.doc_name = row['DocName']
            fec_entity.title = row['Title']
            fec_entity.title_given = row.get('TitleGiven', "")
            fec_entity.date = "%s-%s-%s" % (row['DateYY'], row['DateMM'], row['DateDD'])
            fec_entity.pages = row['Pages']
            fec_entity.is_coded = row['IsCoded']
            fec_entity.is_handwritten = row['IsHandWritten']
            fec_entity.summary = row['Summary']
            fec_entity.note = row['Note']
            fec_entity.internal_note = row['InternalNote']
            fec_entity.confidential = row['NotToPublish']
            fec_entity.place = place

            try:
                fec_entity.save()
                skip = False
            except IntegrityError:
                print "I'm skipping"
                skip = True

            if not skip:
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
                    AssociatedPerson.objects.create(
                        fec_entity=fec_entity,
                        person=person
                    )

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