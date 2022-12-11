# Generated by Django 4.1.3 on 2022-11-25 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0024_index_image_file_hash'),
        ('about', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutindexpage',
            name='mission_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]