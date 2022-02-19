from django.http import request
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView

class AboutAuthorView(TemplateView):
    template_name = 'about/author.html/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['GitHub'] = 'GitHub'
        return context

class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def tech(request):
        return render(request, 'about/tech.html')