# Generated by Django 4.0.6 on 2022-08-09 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapi', '0007_carts_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('order-placed', 'incart'), ('dispatched', 'dispatched'), ('in-transit', 'in-transit')], default='order-placed', max_length=120)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogapi.mobiles')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
