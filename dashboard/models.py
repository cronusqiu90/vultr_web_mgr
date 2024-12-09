from django.db import models

# Create your models here.


class User(models.Model):
    api_token = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    balance = models.FloatField(null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    pending_charges = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    last_payment_date = models.DateTimeField(null=True, blank=True)
    last_payment_amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"User({self.email})"


class Instance(models.Model):
    uuid = models.CharField(max_length=255, null=False, blank=False, primary_key=True)
    os = models.CharField(max_length=255, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)
    disk = models.IntegerField(null=True, blank=True)
    main_ip = models.CharField(max_length=255, null=True, blank=True)
    vcpu_count = models.IntegerField(null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    plan = models.CharField(max_length=255, null=True, blank=True)
    date_created = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    allowed_bandwidth = models.IntegerField(null=True, blank=True)
    netmask_v4 = models.CharField(max_length=255, null=True, blank=True)
    gateway_v4 = models.CharField(max_length=255, null=True, blank=True)
    power_status = models.CharField(max_length=255, null=True, blank=True)
    server_status = models.CharField(max_length=255, null=True, blank=True)
    v6_network = models.CharField(max_length=255, null=True, blank=True)
    v6_main_ip = models.CharField(max_length=255, null=True, blank=True)
    v6_network_size = models.IntegerField(null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    internal_ip = models.CharField(max_length=255, null=True, blank=True)
    kvm = models.CharField(max_length=255, null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)
    tags = models.CharField(max_length=255, null=True, blank=True)
    os_id = models.IntegerField(null=True, blank=True)
    app_id = models.IntegerField(null=True, blank=True)
    image_id = models.CharField(max_length=255, null=True, blank=True)
    firewall_group_id = models.CharField(max_length=255, null=True, blank=True)
    features = models.CharField(max_length=255, null=True, blank=True)
    user_scheme = models.CharField(max_length=255, null=True, blank=True)
    pending_charges = models.FloatField(null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = 'Instance'
        verbose_name_plural = 'Instances'

    def __str__(self):
        return f"Instance({self.hostname})"
