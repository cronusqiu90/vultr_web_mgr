from django.contrib import admin

from .tasks import (
    update_user_information,
    update_all_instance_by_user,
    update_instance_info,
    reboot_vultr_instances
)


@admin.action(description="重启服务器")
def reboot_selected_instances(modeladmin, request, queryset):
    instances = {}
    for instance in queryset:
        if instance.user.api_token not in instances:
            instances[instance.user.api_token] = set()
        instances[instance.user.api_token].add(instance.uuid)
    for api_token, uuids in instances.items():
        reboot_vultr_instances.apply_async(args=[api_token, list(uuids)])


@admin.action(description="更新账号信息")
def update_selected_users(modeladmin, request, queryset):
    for user in queryset:
        update_user_information.apply_async(args=[user.pk])  # type: ignore


@admin.action(description="更新账号所属服务器列表")
def update_instance_list(modeladmin, request, queryset):
    for user in queryset:
        update_all_instance_by_user.apply_async(args=[user.pk])  # type: ignore


@admin.action(description="更新选中服务器信息")
def update_selected_instance(modeladmin, request, queryset):
    for instance in queryset:
        update_instance_info.apply_async(args=[instance.pk])  # type: ignore
