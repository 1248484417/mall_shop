# Generated by Django 2.0.3 on 2019-05-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sadmin', '0010_auto_20190515_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='Super_goods',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('goods_id', models.IntegerField()),
                ('super_id', models.IntegerField()),
            ],
            options={
                'db_table': 'super_goods',
            },
        ),
        migrations.AddField(
            model_name='super',
            name='show_status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='super',
            name='sort',
            field=models.IntegerField(default=0),
        ),
    ]