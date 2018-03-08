import csv
import os
from collections import OrderedDict

from django.conf import settings
from django.core.management import BaseCommand

from records.models import FECEntity

class Command(BaseCommand):
    help = 'Create weekly number of messages.'

    def handle(self, *args, **options):
        fec_first = FECEntity.objects.order_by('date').first()
        fec_last = FECEntity.objects.order_by('date').last()

        fec_records = FECEntity.objects.all()
        countries = OrderedDict()
        total_number = OrderedDict()
        people = OrderedDict()

        for year in range(fec_first.date.year, fec_last.date.year+1):
            for week in range(1, 54):
                week = "%04d week %02d" % (year, week)
                countries[week] = dict()
                people[week] = dict()
                total_number[week] = 0

        for fec in fec_records.iterator():
            if fec.date.strftime('%W') == '00':
                week = fec.date.strftime('%Y week ') + '53'
            else:
                week = fec.date.strftime('%Y week %W')

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

            total_number[week] += 1

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

        # Number of countries
        with open(os.path.join(settings.STATIC_ROOT, 'fec', 'stat', 'fec_number_of_countries.csv'), 'wb') as csvfile:
            fieldnames = ['week', 'country', 'number_of_messages']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, value in countries.iteritems():
                for country, number in value.iteritems():
                    writer.writerow({
                        'week': week,
                        'country': country,
                        'number_of_messages': number
                    })

        # Number of people
        with open(os.path.join(settings.STATIC_ROOT, 'fec', 'stat', 'fec_number_of_people.csv'), 'wb') as csvfile:
            fieldnames = ['week', 'person', 'number_of_messages']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for week, value in people.iteritems():
                for person, number in value.iteritems():
                    writer.writerow({
                        'week': week,
                        'person': person.encode('utf-8'),
                        'number_of_messages': number
                    })