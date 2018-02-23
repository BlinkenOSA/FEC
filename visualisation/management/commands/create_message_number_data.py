import csv
import os

from django.conf import settings
from django.core.management import BaseCommand

from records.models import FECEntity


class Command(BaseCommand):
    help = 'Create weekly number of messages.'

    def handle(self, *args, **options):
        fec_first = FECEntity.objects.order_by('date').first()
        fec_last = FECEntity.objects.order_by('date').last()

        fec_records = FECEntity.objects.all()
        countries = {}
        total_number = {}
        people = {}

        for year in range(fec_first.date.year, fec_last.date.year+1):
            for week in range(0, 54):
                week = "%04d-%02d" % (year, week)
                countries[week] = dict()
                people[week] = dict()
                total_number[week] = 0

        for fec in fec_records.iterator():
            week = fec.date.strftime('%Y-%W')

            for country in fec.countries.all():
                if country.country not in countries[week].keys():
                    countries[week][country.country] = 1
                else:
                    countries[week][country.country] += 1

            for person in fec.associated_people.all():
                if person.person not in people[week].keys():
                    people[week][person.person] = 1
                else:
                    people[week][person.person] += 1

        # Number of reports
        with open(os.path.join(settings.STATIC_ROOT, 'fec', 'stat', 'fec_number_of_reports.csv'), 'wb') as csvfile:
            fieldnames = ['week', 'number_of_messages']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k, v in total_number.iteritems():
                writer.writerow({
                    'week': k,
                    'number_of_messages': v
                })

