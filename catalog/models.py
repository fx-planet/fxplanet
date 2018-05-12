import os

from django.db import models
from django.contrib.postgres.fields import ArrayField


LINK_TYPE_CHOICES = (
        ('image', 'image'),
        ('video', 'video'),
        ('manual', 'manual'),
        ('other', 'other'),
    )


class Category(models.Model):
    name = models.CharField(max_length=128)
    parent = models.ForeignKey(
            'self', on_delete=models.CASCADE, null=True,
            related_name='subcategories')

    class Meta:
        unique_together = ('name', 'parent')
        ordering = ('name',)


class Effect(models.Model):
    name = models.CharField(max_length=128)
    slug = models.SlugField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)
    filename = models.CharField(max_length=128)
    import_path = models.CharField(max_length=255, null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers', null=True, blank=True)
    category = models.ForeignKey(
            Category, on_delete=models.PROTECT, related_name='effects')
    authors = ArrayField(
            base_field=models.CharField(max_length=128), blank=True)
    maintainers = ArrayField(
            base_field=models.CharField(max_length=128), blank=True)
    creation_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    license = models.CharField(max_length=64, blank=True, null=True)

    def image_links(self):
        return self.link_set.filter(kind='image')

    def has_gallery(self):
        return self.link_set.filter(kind='image').count() > 1

    def has_download(self):
        return self.version_set.all().exists()

    def latest_version(self):
        try:
            return self.version_set.order_by('-release_date')[0]
        except IndexError:
            raise Version.DoesNotExist


class Link(models.Model):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
    url = models.URLField()
    kind = models.CharField(
            choices=LINK_TYPE_CHOICES, max_length=32, db_index=True)

    class Meta:
        ordering = ('pk',)


def effect_version_filename(instance, filename):
    return os.path.join(
            os.path.basename(filename),
            instance.release_date.strftime('%Y%m%d'),
            filename)


class Version(models.Model):
    effect = models.ForeignKey(Effect, on_delete=models.CASCADE)
    release_date = models.DateField()
    effect_file = models.FileField(upload_to=effect_version_filename)

    class Meta:
        unique_together = ('effect', 'release_date')
        ordering = ('-release_date',)
