# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Create your views here.
from django.views.generic import TemplateView


class VisualisationView(TemplateView):
    template_name = 'visalisation/vis.html'