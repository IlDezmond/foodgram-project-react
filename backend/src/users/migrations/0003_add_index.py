# Generated by Django 3.2 on 2023-04-09 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20230325_0007'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['author'], name='users_follo_author__5419c6_idx'),
        ),
    ]
