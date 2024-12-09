from typing import Any
from django.contrib import admin
from django.utils import timezone

# Register your models here.
from .models import User, Instance

from .tasks import update_instance_info, update_user_infomation, update_all_instance_by_user

@admin.action(description='重启服务器')
def reboot_selected_instances(modeladmin, request, queryset):
    pass

@admin.action(description='更新账号信息')
def update_selected_users(modeladmin, request, queryset):
    for user in queryset:
        update_user_infomation.apply_async(args=[user.pk]) # type: ignore

@admin.action(description='更新账号所属服务器列表')
def update_instance_list(modeladmin, request, queryset):
    for user in queryset:
        update_all_instance_by_user.apply_async(args=[user.pk]) # type: ignore

@admin.action(description='更新选中服务器信息')
def update_selected_instance(modeladmin, request, queryset):
    for instance in queryset:
        update_instance_info.apply_async(args=[instance.pk]) # type: ignore

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', "api_token", "balance", "pending_charges", "last_payment_date", "last_payment_amount",  "updated_at")
    sorted_by = ('updated_at', 'balance', 'pending_charges',)

    actions = [update_instance_list, update_selected_users]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.updated_at = timezone.now()
        return super().save_model(request, obj, form, change)


@admin.register(Instance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = (
        "user", "uuid", "hostname", "os", "ram", "disk", "status", "power_status", "server_status", "date_created", "updated_at",
    )
    list_filter = ("os", "status", )
    search_fields = ("hostname", "label", "os", "ram", "disk", "status", "power_status", "server_status", "date_created",)

    actions = [update_selected_instance, reboot_selected_instances]

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.updated_at = timezone.now()
        return super().save_model(request, obj, form, change)
