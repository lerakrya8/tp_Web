# Generated by Django 3.1.4 on 2020-12-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image_profile',
            field=models.ImageField(blank=True, default='grandbeauty00.jpg', upload_to='avatar/%y/%m/%d'),
        ),
    ]
