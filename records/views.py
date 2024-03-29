import urllib
from collections import OrderedDict

from braces.views import JSONResponseMixin
from django.urls import reverse
from django.views.generic import DetailView
from iiif_prezi.factory import ManifestFactory
from django.conf import settings

from records.forms import DateRangeSearchForm
from records.models import FECEntity

from haystack.generic_views import FacetedSearchView


class EntitySearchView(FacetedSearchView):
    """My custom search view."""
    template_name = 'records/entity_search.html'
    form_class = DateRangeSearchForm
    load_all = False
    facet_fields = ['place',
                    'associated_people', 'associated_corporations',
                    'countries',
                    'subject_people', 'subject_corporations']
    paginate_by = 24

    def insert_into_data_struct(self, name, value, a_dict):
        if not name in a_dict:
            a_dict[name] = [value]
        else:
            a_dict[name].append(value)

    def get_context_data(self, **kwargs):
        context = super(EntitySearchView, self).get_context_data(**kwargs)
        context['iiif_server'] = settings.BASE_IMAGE_URI
        global_start_date = FECEntity.objects.all().order_by("date").first().date.strftime('%Y-%m-%d')
        global_end_date = FECEntity.objects.all().order_by("-date").first().date.strftime('%Y-%m-%d')
        context['global_start_date'] = global_start_date
        context['global_end_date'] = global_end_date
        context['current_start_date'] = self.request.GET.get('start_date', global_start_date)
        context['current_end_date'] = self.request.GET.get('end_date', global_end_date)

        selected_facets = {}
        sf = context['form'].selected_facets
        for f in sf:
            key, value = f.split(':')
            self.insert_into_data_struct(key, value, selected_facets)
        context['selected_facets'] = selected_facets

        return context

    def get_queryset(self):
        qs = super(EntitySearchView, self).get_queryset()
        return qs.order_by('date_display', 'title_display')


class EntityDetailView(DetailView):
    model = FECEntity
    template_name = 'records/entity_detail.html'

    def get_context_data(self, **kwargs):
        context = super(EntityDetailView, self).get_context_data()
        context['manifest_url'] = self.request.build_absolute_uri(
            reverse('record:manifest', args=[context['fecentity'].id]))

        img_id = urllib.quote_plus(
            "fec/%s/%s_%s_01.jpg" % (self.object.doc_name[:2],
                                  self.object.doc_name[:2],
                                  self.object.doc_name[3:]))

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

        for p in range(1, fec_entity.pages + 1):
            # Create a canvas with uri slug of page-p, and label of Page 1
            canvas_id = "fec-%s-page-%s" % (fec_entity.doc_name, str(p))
            cvs = seq.canvas(ident=canvas_id, label="Page %s" % p)
            underscore_idx = fec_entity.doc_name.find('_')

            image_id = urllib.quote_plus(
                "fec/%s/%s_%s_%02d.jpg" % (
                    fec_entity.doc_name[:underscore_idx],
                    fec_entity.doc_name[:underscore_idx],
                    fec_entity.doc_name[underscore_idx + 1:],
                    p
                )
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
        md["Associated People"] = ", ".join([unicode(ap.person) for ap in fec_entity.associated_people.iterator()])
        md["Associated Corporation"] = ", ".join([unicode(ac.corporation) for ac in
                                                  fec_entity.associated_corporations.iterator()])
        md["Spatial Coverage"] = ", ".join([c.country for c in fec_entity.countries.iterator()])
        md["Coded message"] = 'Yes' if fec_entity.is_coded else 'No'
        md["Handwritten text"] = 'Yes' if fec_entity.is_handwritten else 'No'
        md["Subject People"] = ", ".join([unicode(ap.person) for ap in fec_entity.subject_people.iterator()])
        md["Subject Corporation"] = ", ".join([unicode(ac.corporation) for ac in
                                               fec_entity.subject_corporations.iterator()])
        md["Note"] = fec_entity.note
        md["Place"] = fec_entity.place.place
        return md
