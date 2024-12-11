import requests
from celery import shared_task
from loguru import logger as log

from .models import User, Instance
from .vendor import vultr, dingtalk


# 根据 user.api_token 完善用户个人信息
@shared_task(name="update_user_info", ignore_result=True)
def update_user_information(pk):
    user = User.objects.get(pk=pk)
    try:
        data = vultr.get_account(user.api_token)
        user.update_one(data)
        user.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return


# 更新单台节点信息
@shared_task(name="update_instance_info", ignore_result=True)
def update_instance_info(pk):
    instance = Instance.objects.get(pk=pk)
    try:
        data = vultr.get_instance(instance.user.api_token, instance.uuid)
        instance.update_one(data)
        instance.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return


# 更新用户所属所有节点信息
@shared_task(name="update_all_instance_by_user", igngore_result=True)
def update_all_instance_by_user(pk):
    user = User.objects.get(pk=pk)
    try:
        data = vultr.list_instances(user.api_token)
        for row in data["instances"]:
            uuid = row["id"]
            instance, ok = Instance.objects.get_or_create(uuid=uuid, user=user)
            instance.update_one(row)
            instance.save()
    except requests.exceptions.RequestException as err:
        log.exception(err)
        return


@shared_task(name="reboot_instances", ignore_result=True)
def reboot_vultr_instances(api_token, uuids):
    try:
        vultr.reboot_instances(api_token, uuids)
    except requests.exceptions.RequestException as err:
        log.exception(err)


# 检查节点的状态
@shared_task(name="check_instance_status", ignore_result=True)
def check_instance_status():
    alarm = ""
    # 先更新所有节点信息
    for user in User.objects.all():
        try:
            instances = vultr.list_instances(user.api_token)
            for row in instances["instances"]:
                uuid = row["id"]
                instance, ok = Instance.objects.get_or_create(uuid=uuid, user=user)
                instance.update_one(row)
                instance.save()

                if (
                        instance.status != "active"
                        or instance.server_status != "ok"
                        or instance.power_status != "running"
                ):
                    alarm += f"实例: %-8s  状态: %s  评估: %s  电源: %s\n" % (
                        instance.hostname,
                        instance.status,
                        instance.server_state,
                        instance.power_status,
                    )
                    continue
        except requests.exceptions.RequestException as err:
            log.exception(err)
            continue
    if alarm:
        alarm = "[通知] Vultr 实例状态通知\n\n" + alarm
        r = dingtalk.notify_alarm(alarm)
        log.info(f"alarm: {r}")


# 检查用户余额
@shared_task(name="check_users_remain_credit", ignore_result=True)
def check_users_remain_credit():
    alarm = ""
    for user in User.objects.all():
        try:
            data = vultr.get_account(user.api_token)
            user.update_one(data)
            user.save()
            if user.balance <= user.min_spent_monthly:
                alarm += f"账号: %-30s 余额: %3.2f\n" % (user.email, user.balance)
        except requests.exceptions.RequestException as err:
            log.error(f"failed to update user({user.email}): {err}")
            continue
    if alarm:
        alarm = "[通知] Vultr 账号余额不足通知\n\n" + alarm
        r = dingtalk.notify_alarm(alarm)
        log.info(f"alarm: {r}")
