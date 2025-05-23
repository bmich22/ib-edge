# Generated by Django 5.2 on 2025-05-12 13:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring_sessions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutoringsession',
            name='purchase',
        ),
        migrations.AddField(
            model_name='tutoringsession',
            name='user',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='tutoring_sessions', to=settings.AUTH_USER_MODEL),
        ),
    ]
