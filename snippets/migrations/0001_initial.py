# Generated by Django 2.2.4 on 2021-07-07 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Snippet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('snippet', models.TextField(blank=True, null=True)),
                ('public', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='snippets.Language')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]