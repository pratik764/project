# Generated by Django 5.0.7 on 2024-08-16 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='usertype',
            field=models.CharField(default='user', max_length=100),
        ),
    ]