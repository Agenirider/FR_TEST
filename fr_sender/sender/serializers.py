from rest_framework import serializers

from fr_sender import settings


class FR_API_CLIENT_SERIALIZER(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11, min_length=10, allow_blank=True, default=None)
    def_plmn_code = serializers.CharField(max_length=3, default=None, allow_blank=True)
    tag = serializers.CharField(max_length=30, default=None, allow_blank=True)
    time_zone = serializers.CharField(max_length=5, default=settings.TIME_ZONE, allow_blank=True)


class FR_API_TASK_SERIALIZER(serializers.Serializer):
    start_task = serializers.DateTimeField(default=None)
    end_task = serializers.DateTimeField(default=None)
    message = serializers.CharField(max_length=300, default=None, allow_blank=True)
    tag = serializers.CharField(max_length=30, default=None, allow_blank=True)
    def_plmn_code = serializers.CharField(max_length=3, default=None, allow_blank=True)

