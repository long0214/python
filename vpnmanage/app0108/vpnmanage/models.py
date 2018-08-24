from django.db import models

# Create your models here.

class VpnList(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=30)
    vpn_ip = models.GenericIPAddressField(protocol='IPv4')
    vpn2_ip = models.GenericIPAddressField(protocol='IPv4')
    project_name = models.CharField(max_length=200, null=True)
    user = models.CharField(max_length=30, null=True)
    phone_number = models.CharField(max_length=30, null=True)
    bind_mac = models.CharField(max_length=30, null=True)
