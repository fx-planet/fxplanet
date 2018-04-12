import re
import operator
import functools

from django import forms
from django.db.models import Q


words_re = re.compile('\w+')


def q_factory(x):
    return (
            Q(name__icontains=x) |
            Q(description__icontains=x) |
            Q(category__name__icontains=x) |
            Q(category__parent__name__icontains=x))


class EffectSearchForm(forms.Form):
    q = forms.CharField(required=False)

    def search(self, qs):
        data = self.cleaned_data

        q = data.get('q')

        if q:
            terms = words_re.findall(q)
            q_list = map(q_factory, terms)
            qs = qs.filter(functools.reduce(operator.and_, q_list))
        return qs
