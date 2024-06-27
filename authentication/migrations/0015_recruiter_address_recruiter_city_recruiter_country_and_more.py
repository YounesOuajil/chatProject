# Generated by Django 5.0.4 on 2024-04-29 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0014_user_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiter',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='recruiter_img'),
        ),
        migrations.AddField(
            model_name='recruiter',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
