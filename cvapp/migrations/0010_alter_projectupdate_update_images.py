# Generated by Django 3.2.8 on 2021-11-09 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cvapp', '0009_auto_20211109_2226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectupdate',
            name='update_images',
            field=models.ImageField(blank=True, null=True, unique=True, upload_to='project_updates'),
        ),
    ]