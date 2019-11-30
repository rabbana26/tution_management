# Generated by Django 2.2.7 on 2019-11-30 08:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tution_management_app', '0003_auto_20191130_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='name',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_name', to=settings.AUTH_USER_MODEL),
        ),
    ]
