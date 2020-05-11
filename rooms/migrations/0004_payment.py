# Generated by Django 3.0.5 on 2020-04-21 08:06

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0003_remove_room_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_check_in_date', models.DateField()),
                ('expected_check_out_date', models.DateField()),
                ('check_in_date', models.DateField(blank=True, null=True)),
                ('check_out_date', models.DateField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('WAITING', 'WAITING'), ('CHECKED_IN', 'CHECKED_IN'), ('CHECKED_OUT', 'CHECKED_OUT'), ('PAID', 'PAID'), ('CANCLED', 'CANCLED')], default='WAITING', max_length=20)),
                ('service_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to='rooms.Room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]