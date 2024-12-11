from django.db import models


# Create your models here.


class User(models.Model):
    type_enums = (
        (0, "Server"),
        (1, "Vultr"),
    )
    type_name = models.IntegerField("类型", choices=type_enums, default=0, null=False,
                                    blank=False)
    api_token = models.CharField("Token", max_length=255, null=False, blank=False,
                                 primary_key=True)
    balance = models.FloatField("余额", null=True, blank=True)
    email = models.CharField("Email", max_length=255, null=True, blank=True)
    pending_charges = models.FloatField("待处理账单", null=True, blank=True)
    name = models.CharField("用户名", max_length=255, null=True, blank=True)
    last_payment_date = models.DateTimeField("上次付款时间", null=True, blank=True)
    last_payment_amount = models.FloatField("上次支付金额", null=True, blank=True)
    created_at = models.DateTimeField("创建时间", null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", null=True, blank=True, auto_now=True)
    min_spent_monthly = models.FloatField("月度最低消费", default=0)

    class Meta:
        verbose_name = verbose_name_plural = "账号"

    def __str__(self):
        return f"账号({self.email})"

    def update_one(self, data: dict):
        self.email = data["account"]["email"]
        self.name = data["account"]["name"]
        self.balance = data["account"]["balance"] * -1
        self.pending_charges = data["account"]["pending_charges"] * -1
        self.last_payment_date = data["account"]["last_payment_date"]
        self.last_payment_amount = data["account"]["last_payment_amount"] * -1
        return self


class Instance(models.Model):
    uuid = models.CharField(
        "编号", max_length=255, null=False, blank=False, primary_key=True
    )
    os = models.CharField("系统", max_length=255, null=True, blank=True)
    ram = models.IntegerField("内存", null=True, blank=True)
    disk = models.IntegerField("磁盘", null=True, blank=True)
    main_ip = models.CharField("IPv4", max_length=255, null=True, blank=True)
    vcpu_count = models.IntegerField("vCPU", null=True, blank=True)
    region = models.CharField("地区", max_length=255, null=True, blank=True)
    plan = models.CharField("购买套餐", max_length=255, null=True, blank=True)
    date_created = models.DateTimeField("创建时间", null=True, blank=True)
    # status: active, pending, suspended, resizing
    status = models.CharField("状态", max_length=255, null=True, blank=True)
    allowed_bandwidth = models.IntegerField("每月带宽", null=True, blank=True)
    netmask_v4 = models.CharField("IPv4掩码", max_length=255, null=True, blank=True)
    gateway_v4 = models.CharField("IPv4网关", max_length=255, null=True, blank=True)
    # power_status: running, stopped
    power_status = models.CharField("电源状态", max_length=255, null=True, blank=True)
    # server_status: none, locked, installingbooting, ok
    server_status = models.CharField("服务器状态", max_length=255, null=True, blank=True)
    v6_network = models.CharField("IPv6网络", max_length=255, null=True, blank=True)
    v6_main_ip = models.CharField("IPv6地址", max_length=255, null=True, blank=True)
    v6_network_size = models.IntegerField("IPv6网络规模", null=True, blank=True)
    label = models.CharField("标签", max_length=255, null=True, blank=True)
    internal_ip = models.CharField("内网IP", max_length=255, null=True, blank=True)
    kvm = models.CharField("KVM", max_length=255, null=True, blank=True)
    hostname = models.CharField("主机名", max_length=255, null=True, blank=True)
    tag = models.CharField("标签", max_length=255, null=True, blank=True)
    tags = models.CharField("标签列表", max_length=255, null=True, blank=True)
    os_id = models.IntegerField("OS ID", null=True, blank=True)
    app_id = models.IntegerField("App ID", null=True, blank=True)
    image_id = models.CharField("Image ID", max_length=255, null=True, blank=True)
    firewall_group_id = models.CharField(
        "Firewall GID", max_length=255, null=True, blank=True
    )
    # features: auto_backups, ipv6, ddos_protection
    features = models.CharField("特性列表", max_length=255, null=True, blank=True)
    # user_scheme: root, limited
    user_scheme = models.CharField("用户权限", max_length=255, null=True, blank=True)
    pending_charges = models.FloatField("待处理的账单", null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = verbose_name_plural = "服务器实例"

    def __str__(self):
        return f"节点({self.hostname})"

    def update_one(self, data: dict):
        self.os = data["instance"]["os"]
        self.ram = data["instance"]["ram"]
        self.disk = data["instance"]["disk"]
        self.main_ip = data["instance"]["main_ip"]
        self.vcpu_count = data["instance"]["vcpu_count"]
        self.region = data["instance"]["region"]
        self.plan = data["instance"]["plan"]
        self.date_created = data["instance"]["date_created"]
        self.status = data["instance"]["status"]
        self.allowed_bandwidth = data["instance"]["allowed_bandwidth"]
        self.netmask_v4 = data["instance"]["netmask_v4"]
        self.gateway_v4 = data["instance"]["gateway_v4"]
        self.power_status = data["instance"]["power_status"]
        self.server_status = data["instance"]["server_status"]
        self.v6_network = data["instance"]["v6_network"]
        self.v6_main_ip = data["instance"]["v6_main_ip"]
        self.v6_network_size = data["instance"]["v6_network_size"]
        self.label = data["instance"]["label"]
        self.internal_ip = data["instance"]["internal_ip"]
        self.kvm = data["instance"]["kvm"]
        self.hostname = data["instance"]["hostname"]
        self.tag = data["instance"]["tag"]
        self.tags = data["instance"]["tags"]
        self.os_id = data["instance"]["os_id"]
        self.app_id = data["instance"]["app_id"]
        self.image_id = data["instance"]["image_id"]
        self.firewall_group_id = data["instance"]["firewall_group_id"]
        self.features = data["instance"]["features"]
        self.user_scheme = data["instance"]["user_scheme"]
        if "pending_charges" in data["instance"]:
            self.pending_charges = data["instance"]["pending_charges"]
