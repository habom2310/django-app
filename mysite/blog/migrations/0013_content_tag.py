# Generated by Django 3.2.9 on 2021-11-22 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_content_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='tag',
            field=models.ManyToManyField(blank=True, related_name='friends', to='blog.Genre'),
        ),
    ]
