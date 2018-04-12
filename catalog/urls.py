from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path(
        'detail/<str:slug>/', views.EffectDetailView.as_view(),
        name='effect-detail'),
    path(
        'latest/', views.LatestEffectsListView.as_view(),
        name='latest-effects'),
    path(
        'latest/<int:category>/', views.LatestEffectsListView.as_view(),
        name='latest-effects-by-category'),
    ]
