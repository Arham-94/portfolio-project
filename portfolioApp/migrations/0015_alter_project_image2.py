# Generated by Django 5.2.1 on 2025-06-15 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolioApp', '0014_alter_project_image2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='image2',
            field=models.ImageField(blank=True, default=None, upload_to='projects/'),
        ),
    ]
