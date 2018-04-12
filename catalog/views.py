from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

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
    paginate_by = 9
    template_name = 'latest.html'
    ordering = ('-created_at',)

    def get_queryset(self):
        qs = super(LatestEffectsListView, self).get_queryset()
        if 'category' in self.kwargs:
            cat = self.kwargs['category']
            qs = qs.filter(Q(category=cat) | Q(category__parent=cat))
        return qs

    def get_context_data(self):
        data = super(LatestEffectsListView, self).get_context_data()
        if 'category' in self.kwargs:
            cat = Category.objects.get(pk=self.kwargs['category'])
            data['category'] = cat
            data['subcategories'] = Category.objects.filter(parent=cat)
        else:
            data['subcategories'] = Category.objects.filter(
                                parent__isnull=True)
        return data


class EffectDetailView(DetailView):
    model = Effect
