import csv
import json
import os
from collections import OrderedDict

import itertools
from django.conf import settings
from django.core.management import BaseCommand

from records.models import FECEntity


class Command(BaseCommand):
    help = 'Create graph for number of messages.'

    def handle(self, *args, **options):
        fec_records = FECEntity.objects.all()
        nodes = []
        edges = []

        for fec in fec_records.iterator():
            for person in fec.associated_people.all():
                nodes.append(
                    {
                        'data': {
                            'id': '%d' % int(person.id),
                            'label': person.person
                        }
                    }
                )

            associated_people = set([int(person.id) for person in fec.associated_people.all()])
            combinations = list(itertools.combinations(associated_people, 2))
            for combination in combinations:
                edges.append(
                    {
                        'data': {
                            'id': '%d-%d' % (combination[0], combination[1]),
                            'source': '%d' % combination[0],
                            'target': '%d' % combination[1]
                        }
                    }
                )

        cyto_data = {
            "nodes": nodes,
            "edges": edges
        }

        with open(os.path.join(settings.STATIC_ROOT, 'fec', 'stat', 'fec_graph.json'), 'w') as jsonfile:
            json.dump(cyto_data, jsonfile)
