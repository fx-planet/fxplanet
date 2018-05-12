from django.contrib import admin
from django.db.models import Count
from .models import Category, Effect


class HasEffectsFilter(admin.SimpleListFilter):
    title = 'has effects'
    parameter_name = 'has_effects'

    def lookups(self, request, model_admin):
        return (('0', 'No'), ('1', 'Yes'))

    def queryset(self, request, queryset):
        value = self.value()
        queryset = queryset.annotate(effects_count=Count('effects'))
        if value == '0':
            return queryset.filter(effects_count=0)
        elif value == '1':
            return queryset.filter(effects_count__gt=0)


class ParentFilter(admin.SimpleListFilter):
    title = 'parent'
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        qs = model_admin.model.objects.annotate(
            subcat_count=Count('subcategories')).filter(subcat_count__gt=0)
        return [(x.pk, x.name) for x in qs]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(parent=value)
        return queryset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'path', 'effects_count')
    list_filter = (HasEffectsFilter, ParentFilter)
    search_fields = ('name', 'parent__name',)

    def effects_count(self, obj):
        return obj.effects.count()

    def path(self, obj):
        return '/'.join(map(str, obj.path))


class CategoryFilter(admin.SimpleListFilter):
    title = 'category'
    parameter_name = 'category'

    def lookups(self, request, model_admin):
        effects_qs = model_admin.get_queryset(request)
        qs = Category.objects.filter(
                pk__in=effects_qs.values('category'))
        return [(x.pk, x.path_names) for x in qs]

    def queryset(self, request, queryset):
        value = self.value()
        if value:
            queryset = queryset.filter(category=value)
        return queryset


@admin.register(Effect)
class EffectAdmin(admin.ModelAdmin):
    search_fields = ('name', 'category__name', 'filename', 'description')
    list_display = (
            'name', 'category', 'filename', 'creation_date', 'created_at')
    list_filter = (CategoryFilter, 'created_at', 'creation_date', 'license')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            names = [
                x.name for x in obj._meta.get_fields() if not x.is_relation]
            return names+['category']
        return []
