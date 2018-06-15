import os
import requests
import urllib

from django.conf import settings
from django.core.management import BaseCommand
from records.models import FECEntity


class Command(BaseCommand):
    help = 'Create FEC Thumbnails.'

    def handle(self, *args, **options):
        entities = FECEntity.objects.all()
        for entity in entities:
            local_filename = os.path.join(settings.MEDIA_ROOT, 'thumbnails', entity.doc_name[:2], '%s.jpg' % entity.doc_name)
            doc_id = urllib.quote_plus('%s/%s/%s.jpg' % ('fec', entity.doc_name[:2], entity.doc_name))
            url = "%s%s/%s" % (settings.BASE_IMAGE_URI, doc_id, "200,200,700,533/full/0/gray.jpg")

            print("Downloading thumbnail: %s" % url)
            r = requests.get(url, allow_redirects=True)
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'thumbnails', entity.doc_name[:2])):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'thumbnails', entity.doc_name[:2]))
            open(local_filename, 'wb').write(r.content)
