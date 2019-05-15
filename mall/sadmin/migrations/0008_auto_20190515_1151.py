# Generated by Django 2.0.3 on 2019-05-15 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sadmin', '0007_discourse_detail_user_head_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discourse_comment',
            old_name='total_zan',
            new_name='collect_sum',
        ),
        migrations.RenameField(
            model_name='discourse_comment',
            old_name='pic',
            new_name='user_address',
        ),
        migrations.AddField(
            model_name='discourse_comment',
            name='evaluate_sum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='discourse_comment',
            name='user_head_image',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='discourse_comment',
            name='user_profession',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
