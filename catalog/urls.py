from django.urls import path
from django.views.generic.base import RedirectView
from . import views


urlpatterns = [
    path('', views.index),
    path(
        'effect/<str:slug>/', views.EffectDetailView.as_view(),
        name='effect-detail'),
    path(
        'effect/<str:slug>/download/', views.download, name='effect-download'),
    path(
        'effects/', views.LatestEffectsListView.as_view(),
        name='latest-effects'),
    path(
        'effects/<int:category>/', views.LatestEffectsListView.as_view(),
        name='latest-effects-by-category'),
    path(
        'detail/<str:slug>/',
        RedirectView.as_view(pattern_name='effect-detail', permanent=True)),
    path(
        'latest/<int:category>/',
        RedirectView.as_view(
            pattern_name='latest-effects-by-category', permanent=True)),
    path(
        'latest/',
        RedirectView.as_view(
            pattern_name='latest-effects', permanent=True)),
    ]
