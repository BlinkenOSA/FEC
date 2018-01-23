import urllib
from collections import OrderedDict

from django.contrib.staticfiles.templatetags.staticfiles import static

from braces.views import JSONResponseMixin
from django.urls import reverse
from django.views.generic import DetailView
from iiif_prezi.factory import ManifestFactory
from django.conf import settings

from records.models import FECEntity


class EntityDetailView(DetailView):
    model = FECEntity
    template_name = 'entity_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntityDetailView, self).get_context_data()
        context['manifest_url'] = self.request.build_absolute_uri(
            reverse('record:manifest', args=[context['fecentity'].id]))

        img_id = urllib.quote_plus(
            "fec/%s/%s_%s.jpg" % (self.object.doc_name[:2],
                                  self.object.doc_name[:2],
                                  str(int(self.object.doc_name[3:]))))

        context['header_img'] = "%s%s/full/full/0/default.jpg" % (
            settings.BASE_IMAGE_URI,
            img_id
        )

        return context


class EntityManifestView(JSONResponseMixin, DetailView):
    model = FECEntity

    def get(self, request, *args, **kwargs):
        fec_entity = self.get_object()

        fac = ManifestFactory()
        fac.set_base_prezi_uri(getattr(settings, 'BASE_PREZI_URI', 'http://127.0.0.1:8000/'))

        # Default Image API information
        fac.set_base_image_uri(getattr(settings, 'BASE_IMAGE_URI', 'http://127.0.0.1:8182/iiif/2/'))
        fac.set_iiif_image_info(2.0, 2)
        fac.set_debug("error")

        manifest = fac.manifest(label=fec_entity.title)

        manifest.set_metadata(self.assemble_metadata(fec_entity))
        manifest.viewingDirection = "left-to-right"

        manifest.attribution = 'Radio Free Europe/Free Europe Committee - Encrypted Telex Communication<br/>' \
                               'Vera & Donald Blinken Open Society Archives'

        seq = manifest.sequence()

        for p in range(1, fec_entity.pages+1):
            # Create a canvas with uri slug of page-p, and label of Page 1
            canvas_id = "fec-%s-page-%s" % (fec_entity.doc_name, str(p))
            cvs = seq.canvas(ident=canvas_id, label="Page %s" % p)
            image_id = urllib.quote_plus(
                "fec/%s/%s_%s.jpg" % (fec_entity.doc_name[:2],
                                      fec_entity.doc_name[:2],
                                      str(int(fec_entity.doc_name[3:])+p-1))
            )
            cvs.set_image_annotation(image_id, iiif=True)

        return self.render_json_response(manifest.toJSON(top=True))

    def assemble_metadata(self, fec_entity):
        md = OrderedDict()
        md['Title'] = fec_entity.title
        md['Date'] = fec_entity.date
        md['Given Title'] = fec_entity.title_given
        md['Number of Pages'] = str(fec_entity.pages)
        md['Summary'] = fec_entity.summary
        md["Associated People"] = ", ".join([ap.person for ap in fec_entity.associated_people.iterator()])
        md["Associated Corporation"] = ", ".join([ac.corporation for ac in
                                                  fec_entity.associated_corporations.iterator()])
        md["Spatial Coverage"] = ", ".join([c.country for c in fec_entity.countries.iterator()])
        md["Coded message"] = 'Yes' if fec_entity.is_coded else 'No'
        md["Handwritten text"] = 'Yes' if fec_entity.is_handwritten else 'No'
        md["Subject People"] = ", ".join([ap.person for ap in fec_entity.subject_people.iterator()])
        md["Subject Corporation"] = ", ".join([ac.corporation for ac in
                                                  fec_entity.subject_corporations.iterator()])
        md["Note"] = fec_entity.note
        md["Place"] = fec_entity.place.place
        return md
