# Generated by Django 3.1.1 on 2020-10-08 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0022_uploadedimage'),
        ('blog', '0007_auto_20201008_1740'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleBlogPage',
            fields=[
                ('blogdetailpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blog.blogdetailpage')),
                ('subtitle', models.CharField(blank=True, max_length=100, null=True)),
                ('intro_image', models.ForeignKey(blank=True, help_text='Best size for this image is 1400x400', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtailimages.image')),
            ],
            options={
                'abstract': False,
            },
            bases=('blog.blogdetailpage',),
        ),
    ]