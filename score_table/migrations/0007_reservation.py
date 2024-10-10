# Generated by Django 5.1.1 on 2024-10-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('score_table', '0006_rename_created_at_fujitaranking_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50)),
                ('reservation_number', models.CharField(max_length=10, unique=True)),
                ('is_checked_in', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
