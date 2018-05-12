from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from .forms import EffectSearchForm
from .models import Effect, Category


def index(request):
    ctx = {
            'latest_effects': Effect.objects.order_by('-created_at'),
            'subcategories': Category.objects.filter(parent__isnull=True),
            }
    return render(request, 'index.html', ctx)


@require_POST
def download(request, slug):
    obj = get_object_or_404(Effect, slug=slug)
    resp = HttpResponse(obj.latest_version().effect_file)
    resp['Content-Disposition'] = 'attachment; filename=%s' % obj.filename
    resp['Content-Type'] = 'text/x-opencl-src'
    return resp


class LatestEffectsListView(ListView):
    model = Effect
    template_name = 'latest.html'
    ordering = ('-created_at',)

    def get_queryset(self):
        qs = super(LatestEffectsListView, self).get_queryset()
        if 'category' in self.kwargs:
            cat = self.kwargs['category']
            qs = qs.filter(Q(category=cat) | Q(category__parent=cat))
        form = EffectSearchForm(data=self.request.GET)
        self.form = form
        if form.is_valid():
            qs = form.search(qs)
        return qs

    def get_context_data(self):
        data = super(LatestEffectsListView, self).get_context_data()
        data['toplevel_categories'] = Category.objects.filter(
                                                parent__isnull=True)

        if 'category' in self.kwargs:
            cat = Category.objects.get(pk=self.kwargs['category'])
            data['category'] = cat
            data['subcategories'] = Category.objects.filter(parent=cat)
        else:
            data['subcategories'] = Category.objects.filter(
                                parent__isnull=True)
        data['search'] = self.form.data
        return data


class EffectDetailView(DetailView):
    model = Effect

    # def get_success_url(self):
    #     return reverse('notes-list')

    def get_context_data(self, **kwargs):
        data = super(EffectDetailView, self).get_context_data(**kwargs)
        data['toplevel_categories'] = Category.objects.filter(
                                                parent__isnull=True)
        return data
