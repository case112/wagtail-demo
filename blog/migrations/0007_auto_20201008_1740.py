# Generated by Django 3.1.1 on 2020-10-08 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_blogdetailpage_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blogdetailpage',
            old_name='blog_image',
            new_name='banner_image',
        ),
    ]