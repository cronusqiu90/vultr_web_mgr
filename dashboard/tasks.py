import requests
from celery import shared_task
from loguru import logger as log

from .models import User, Instance


vultr_api = "https://api.vultr.com/v2/"




@shared_task(name="update_user_info", ignore_result=True)
def update_user_infomation(pk):
    user = User.objects.get(pk=pk)
    try:
        resp = requests.get(
            url="https://api.vultr.com/v2/account", 
            headers={"Authorization": f"Bearer {user.api_token }"},
            timeout=55
        )
        resp.raise_for_status()
        data = resp.json()
        user.email = data['account']['email']
        user.name = data['account']['name']
        user.balance = data['account']['balance']
        user.last_payment_date = data['account']['last_payment_date']
        user.last_payment_amount = data['account']['last_payment_amount']
        user.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return


@shared_task(name="update_instance_info", ignore_result=True)
def update_instance_info(pk):
    instance = Instance.objects.get(pk=pk)

    try:
        resp = requests.get(
            url=f"https://api.vultr.com/v2/instances/{instance.uuid}",
            headers={"Authorization": f"Bearer {instance.user.api_token}"},
            timeout=55
        )
        resp.raise_for_status()
        data = resp.json()
        instance.os = data['instance']['os']
        instance.ram = data['instance']['ram']
        instance.disk = data['instance']['disk']
        instance.main_ip = data['instance']['main_ip']
        instance.vcpu_count = data['instance']['vcpu_count']
        instance.region = data['instance']['region']
        instance.plan = data['instance']['plan']
        instance.date_created = data['instance']['date_created']
        instance.status = data['instance']['status']
        instance.allowed_bandwidth = data['instance']['allowed_bandwidth']
        instance.netmask_v4 = data['instance']['netmask_v4']
        instance.gateway_v4 = data['instance']['gateway_v4']
        instance.power_status = data['instance']['power_status']
        instance.server_status = data['instance']['server_status']
        instance.v6_network = data['instance']['v6_network']
        instance.v6_main_ip = data['instance']['v6_main_ip']
        instance.v6_network_size = data['instance']['v6_network_size']
        instance.label = data['instance']['label']
        instance.internal_ip = data['instance']['internal_ip']
        instance.kvm = data['instance']['kvm']
        instance.hostname = data['instance']['hostname']
        instance.tag = data['instance']['tag']
        instance.tags = data['instance']['tags']
        instance.os_id = data['instance']['os_id']
        instance.app_id = data['instance']['app_id']
        instance.image_id = data['instance']['image_id']
        instance.firewall_group_id = data['instance']['firewall_group_id']
        instance.features = data['instance']['features']
        instance.user_scheme = data['instance']['user_scheme']
        if "pending_charges" in data['instance']:
            instance.pending_charges = data['instance']['pending_charges']
        instance.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return


@shared_task(name="update_all_instance_by_user", igngore_result=True)
def update_all_instance_by_user(pk):
    user = User.objects.get(pk=pk)
    try:
        resp = requests.get(
            url="https://api.vultr.com/v2/instances",
            headers={"Authorization": f"Bearer {user.api_token }"},
            timeout=55
        )
        resp.raise_for_status()
        data = resp.json()
        for row in data['instances']:
            uuid = row['uuid']
            instance, ok = Instance.objects.get_or_create(uuid=uuid, user=user)
            instance.os = row['os']
            instance.ram = row['ram']
            instance.disk = row['disk']
            instance.main_ip = row['main_ip']
            instance.vcpu_count = row['vcpu_count']
            instance.region = row['region']
            instance.plan = row['plan']
            instance.date_created = row['date_created']
            instance.status = row['status']
            instance.allowed_bandwidth = row['allowed_bandwidth']
            instance.netmask_v4 = row['netmask_v4']
            instance.gateway_v4 = row['gateway_v4']
            instance.power_status = row['power_status']
            instance.server_status = row['server_status']
            instance.v6_network = row['v6_network']
            instance.v6_main_ip = row['v6_main_ip']
            instance.v6_network_size = row['v6_network_size']
            instance.label = row['label']
            instance.internal_ip = row['internal_ip']
            instance.kvm = row['kvm']
            instance.hostname = row['hostname']
            instance.tag = row['tag']
            instance.tags = row['tags']
            instance.os_id = row['os_id']
            instance.app_id = row['app_id']
            instance.image_id = row['image_id']
            instance.firewall_group_id = row['firewall_group_id']
            instance.features = row['features']
            instance.user_scheme = row['user_scheme']
            if "pending_charges" in row:
                instance.pending_charges = row['pending_charges']
            instance.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return

@shared_task(name="cleanup_tasks", ignore_result=True)
def cleanup_tasks():
    pass
