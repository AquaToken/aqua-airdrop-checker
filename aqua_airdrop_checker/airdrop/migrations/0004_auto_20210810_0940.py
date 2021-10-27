# Generated by Django 3.2.6 on 2021-08-10 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airdrop', '0003_airdroppayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airdropaccount',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='airdropaccount',
            name='public_key',
            field=models.CharField(db_index=True, max_length=56, unique=True),
        ),
        migrations.AlterField(
            model_name='airdroppayment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
