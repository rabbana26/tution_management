# Generated by Django 2.2.7 on 2019-11-30 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tution_management_app', '0005_auto_20191130_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='subjects',
            field=models.ManyToManyField(blank=True, to='tution_management_app.Subject'),
        ),
    ]