from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.db.models import Q

from .models import Effect, Category


def index(request):
    ctx = {
            'latest_effects': Effect.objects.order_by('-created_at'),
            }
    return render(request, 'index.html', ctx)


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
