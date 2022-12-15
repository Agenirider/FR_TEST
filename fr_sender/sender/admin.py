from django.contrib import admin
from django.contrib.auth.models import Group

from sender.models import (FR_APIClient,
                           FR_APIDistributionTask,
                           FR_APIMessage)


@admin.register(FR_APIClient)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'phone_number',
                    'def_plmn_code',
                    'tag',
                    'time_zone',
                    )
    search_fields = ['phone_number', 'def_plmn_code']
    ordering = ("id",)


@admin.register(FR_APIDistributionTask)
class DistributionTaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'create_task',
                    'modified_task',
                    'start_task',
                    'end_task',
                    'message',
                    'def_plmn_code',
                    'tag'
                    )
    search_fields = ['message']
    ordering = ("id",)


@admin.register(FR_APIMessage)
class MessageTaskAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'creation_time',
                    'status',
                    'distribution_task',
                    'client',
                    "should_be_send"
                    )
    search_fields = ['message']
    ordering = ("id",)

    def should_be_send(self, instance):
        return instance.distribution_task.start_task


admin.site.unregister(Group)

#
# class DistributionLog(models.Model):
#     pass
#
#
# class DistributionStats(models.Model):
#     pass
