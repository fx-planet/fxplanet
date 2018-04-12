from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag
def page_query_string(page_number, query_data):
    query_data = query_data or {}
    try:
        query_data = query_data.copy()
    except AttributeError:
        query_data = QueryDict(mutable=True)
    query_data['page'] = page_number
    return query_data.urlencode()
