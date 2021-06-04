# Generated by Django 3.0.3 on 2020-02-18 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='article', max_length=32)),
                ('content', models.TextField(null=True)),
            ],
        ),
    ]
