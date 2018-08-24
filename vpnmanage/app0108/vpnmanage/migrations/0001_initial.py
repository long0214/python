# Generated by Django 2.0 on 2018-01-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VpnList',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('account', models.CharField(max_length=30)),
                ('vpn_ip', models.GenericIPAddressField(protocol='IPv4')),
                ('vpn_2ip', models.GenericIPAddressField(protocol='IPv4')),
                ('project_name', models.CharField(max_length=200)),
                ('default_password', models.CharField(max_length=30)),
                ('user', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('dev_outip', models.GenericIPAddressField(protocol='IPv4')),
                ('use_proxy_svn', models.BooleanField()),
                ('bind_ip', models.GenericIPAddressField(protocol='IPv4')),
                ('bind_mac', models.CharField(max_length=50)),
            ],
        ),
    ]