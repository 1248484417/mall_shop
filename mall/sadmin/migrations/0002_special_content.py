# Generated by Django 2.0.3 on 2019-05-14 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sadmin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='special',
            name='content',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]