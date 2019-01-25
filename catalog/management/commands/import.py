import os
import json
import requests

from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from dateutil.parser import parse as parse_dt
from io import BytesIO

from django.core.files import File
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils.text import slugify

from catalog.models import Effect, Category, Version


def todate(x):
    if x:
        return parse_dt(x)
    else:
        return None


class Command(BaseCommand):
    help = 'import effects using json metadata source'

    def add_arguments(self, parser):
        parser.add_argument('metadata_path', type=str)
        parser.add_argument('replace', type=bool, default=False)

    def handle(self, *args, **kw):
        with open(kw['metadata_path']) as fh:
            buf = json.load(fh)

        def get_unique_id(x):
            parts = x['path'].split('/')
            name = os.path.splitext(parts[-1])[0]
            # return '-'.join(map(slugify, parts[:-1]+[name]))
            return slugify(name)

        items = buf['items']
        items_cnt = len(items)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip/deflate',
            'User-Agent': 'HTTPie/0.9.9'
        }

        executor = ThreadPoolExecutor(max_workers=20)
        link_types_as = []

        def download_and_save_cover_image(url, obj):
            print("Fetching %s" % url)
            r = requests.get(url, headers=headers)
            if obj.cover_image:
                obj.cover_image.delete()
            obj.cover_image.save(
                    os.path.basename(url),
                    File(BytesIO(r.content)))

        def fetch_contentype(link):
            r = requests.head(link.url, headers=headers)
            return (link, r.headers['content-type'])

        imported_objs = []

        for i, x in enumerate(items):
            slug = get_unique_id(x)
            filename = x['filename']
            name = x['name']
            print('Importing %s/%s: %s' % (i+1, items_cnt, name))

            catname = x['category']
            subcatname = x.get('subcategory')

            cat = Category.objects.get_or_create(
                    name=catname, parent=None)[0]
            if subcatname:
                subcat = Category.objects.get_or_create(
                    name=subcatname, parent=cat)[0]
            else:
                subcat = cat

            obj, created = Effect.objects.get_or_create(slug=slug, defaults={
                'category': subcat, 'name': name, 'filename': filename,
                'authors': [], 'maintainers': []})
            if not created:
                obj.category = subcat
                obj.name = name
                obj.filename = filename
            obj.description = x['description']
            obj.import_path = x['path']
            obj.authors = x.get('author') or []
            obj.maintainers = x.get('maintainer') or []
            obj.creation_date = todate(x.get('created'))
            obj.license = x.get('license')
            obj.save()
            imported_objs.append(obj)

            links = x.get('see') or []

            for url in links:
                link = obj.link_set.get_or_create(
                        url=url, defaults={'kind': 'other'})[0]
                link_types_as.append(executor.submit(fetch_contentype, link))

            release_date = todate(x.get('released'))
            if not obj.version_set.filter(release_date=release_date).exists():
                ver = Version(effect=obj, release_date=release_date)
                print(obj.filename)
                ver.effect_file.save(
                        obj.filename, File(open(x['abspath'], 'rb')))
                ver.save()

        print("Updating links...")
        for res in as_completed(link_types_as):
            link, mime = res.result()
            link.media_type = mime
            if mime.startswith('image/'):
                link.kind = 'image'
            elif mime.startswith('video/'):
                link.kind = 'video'
            else:
                link.kind = 'other'
            link.save()

        print("Fetching cover images...")

        asyncs = []

        for obj in imported_objs:
            try:
                link = obj.link_set.filter(kind='image')[0]
            except IndexError:
                continue
            else:
                asyncs.append(executor.submit(
                    download_and_save_cover_image, link.url, obj))

        wait(asyncs)

        if kw['replace']:
            print("Removing effects not existing in the import file")
            to_delete = Effect.objects.exclude(pk__in=imported_objs)
            print("%s effects to be removed...", to_delete.count())
            for obj in to_delete:
                if obj.cover_image:
                    obj.cover_image.delete(save=False)
                obj.delete()
            print("Effects were removed.")

            print("Removing empty categories...")
            while True:
                categories = Category.objects.annotate(
                    sub_cnt=Count('subcategories'),
                    fx_cnt=Count('effects')).filter(sub_cnt=0, fx_cnt=0)
                if categories:
                    print("Found %s categories without child items")
                    names = list(categories.values_list('pk', 'name'))
                    categories.delete()
                    print("Deleted categories: %s", names)
                else:
                    print("No more categories to delete.")
                    break
            print("Finished removing categories.")

        print("Done.")
