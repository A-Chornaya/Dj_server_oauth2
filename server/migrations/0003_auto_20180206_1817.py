# Generated by Django 2.0.1 on 2018-02-06 18:17

from django.db import migrations, models
import server.generator


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_auto_20180204_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesstoken',
            name='expires',
            field=models.DateTimeField(default=server.generator.get_token_expiry),
        ),
        migrations.AlterField(
            model_name='accesstoken',
            name='scope',
            field=models.CharField(choices=[('EMAIL', 'email'), ('FIRSTNAME', 'first_name'), ('LASNAME', 'last_name')], max_length=50),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_id',
            field=models.CharField(default=server.generator.short_token, max_length=255),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_secret',
            field=models.CharField(default=server.generator.long_token, max_length=255),
        ),
        migrations.AlterField(
            model_name='grant',
            name='scope',
            field=models.CharField(choices=[('EMAIL', 'email'), ('FIRSTNAME', 'first_name'), ('LASNAME', 'last_name')], max_length=50),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='login',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
