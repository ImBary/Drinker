# Generated by Django 5.1.7 on 2025-03-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DrinkerApp', '0003_drink_complexity_drink_strength_drink_taste_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drink',
            name='short_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
