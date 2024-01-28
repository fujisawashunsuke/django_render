# Generated by Django 4.1.7 on 2023-12-28 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0004_postapp_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postapp',
            old_name='image',
            new_name='image1',
        ),
        migrations.AddField(
            model_name='postapp',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='投稿画像'),
        ),
        migrations.AddField(
            model_name='postapp',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='投稿画像'),
        ),
    ]
