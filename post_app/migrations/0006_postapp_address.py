# Generated by Django 4.1.7 on 2024-01-13 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0005_rename_image_postapp_image1_postapp_image2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='postapp',
            name='address',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]