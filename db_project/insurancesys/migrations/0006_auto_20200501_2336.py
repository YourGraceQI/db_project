# Generated by Django 3.0.5 on 2020-05-01 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurancesys', '0005_auto_20200501_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policy',
            name='policy_status',
            field=models.CharField(choices=[('C', 'policy is current'), ('P', 'policy is expired'), ('PD', 'policy is pending payment')], default='PD', max_length=2),
        ),
        migrations.AlterField(
            model_name='policy',
            name='premium_amount',
            field=models.DecimalField(decimal_places=2, max_digits=22, null=True),
        ),
    ]
