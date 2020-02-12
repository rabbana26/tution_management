# Generated by Django 2.2.7 on 2019-11-30 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tution_management_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('subjects', models.ManyToManyField(to='tution_management_app.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='student_name', to=settings.AUTH_USER_MODEL)),
                ('teachers', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]