from typing import Any
from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import User, Instance

from .tasks import (
    update_instance_info,
    update_user_information,
    update_all_instance_by_user,
)

admin.site.site_header = "Dashboard"  # 设置header
admin.site.site_title = "Dashboard"  # 设置title
admin.site.index_title = "Dashboard"


@admin.action(description="重启服务器")
def reboot_selected_instances(modeladmin, request, queryset):
    pass


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


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "type_name",
        "email",
        "balance",
        "min_spent_monthly",
        "pending_charges",
        "last_payment_date",
        "last_payment_amount",
        "updated_at",
    )
    list_display_links = ("email",)
    list_filter = ("type_name", )
    sorted_by = ("balance",)
    readonly_fields = (
        "email",
        "name",
        "balance",
        "pending_charges",
        "last_payment_date",
        "last_payment_amount",
    )

    actions = [update_instance_list, update_selected_users]

    def save_model(self, request: Any, obj: User, form: Any, change: Any) -> None:
        obj.updated_at = timezone.now()
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:  # type: ignore
            return True
        return False


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = (
        "hostname",
        "os",
        "ram",
        "disk",
        "status",
        "power_status",
        "server_status",
        "date_created",
        "updated_at",
    )
    list_filter = ("os", "status", "power_status", "server_status")
    search_fields = (
        "hostname",
        "os",
        "user__email",
    )
    readonly_fields = (
        "uuid",
        "os",
        "ram",
        "disk",
        "main_ip",
        "vcpu_count",
        "region",
        "plan",
        "date_created",
        "status",
        "allowed_bandwidth",
        "netmask_v4",
        "gateway_v4",
        "power_status",
        "server_status",
        "v6_network",
        "v6_main_ip",
        "v6_network_size",
        "label",
        "internal_ip",
        "kvm",
        "hostname",
        "tag",
        "tags",
        "os_id",
        "app_id",
        "image_id",
        "firewall_group_id",
        "features",
        "user_scheme",
        "pending_charges",
        "user",
        "updated_at",
    )
    actions = [update_selected_instance, reboot_selected_instances]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.updated_at = timezone.now()
        return super().save_model(request, obj, form, change)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:  # type: ignore
            return True
        return False
