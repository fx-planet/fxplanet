# Generated by Django 2.0.4 on 2019-01-24 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20180419_0810'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='link',
            name='media_type',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='catalog.Category'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='effects', to='catalog.Category'),
        ),
        migrations.AlterField(
            model_name='effect',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='synced at'),
        ),
    ]
