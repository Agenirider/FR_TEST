import re
from datetime import datetime

from django.db import models
from typing.re import Pattern

from fr_sender import settings

from django.core.validators import RegexValidator

PHONE_RE_PATTERN: Pattern = re.compile(r'^7*(?P<def_code>\d{3})(?P<phone_number>\d{7})$')


class FR_APIClient(models.Model):
    phone_regex = RegexValidator(regex=PHONE_RE_PATTERN)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False, null=False)
    def_plmn_code = models.CharField(max_length=3, blank=True, null=True)
    tag = models.CharField(max_length=30, blank=True, null=True)
    time_zone = models.CharField(max_length=5, default=settings.TIME_ZONE)

    def __str__(self):
        return f"7{self.def_plmn_code}{self.phone_number} {self.time_zone} {'#' + self.tag if self.tag else ''}"

    def save(self, *args, **kwargs) -> None:
        if self.phone_number and not self.def_plmn_code:
            phone_parts: Pattern = re.search(PHONE_RE_PATTERN, self.phone_number.strip())

            def_code: str = phone_parts.group('def_code')
            phone_number: str = phone_parts.group('phone_number')
            if def_code:
                self.def_plmn_code = def_code

            if phone_number:
                self.phone_number = phone_number

        return super(FR_APIClient, self).save(*args, **kwargs)

    class Meta:
        db_table = 'clients'
        verbose_name_plural = 'Clients'


class FR_APIDistributionTask(models.Model):
    create_task = models.DateTimeField(blank=False, null=False)
    modified_task = models.DateTimeField(blank=False, null=True)
    start_task = models.DateTimeField(blank=True, null=True)
    end_task = models.DateTimeField(blank=True, null=True)
    message = models.CharField(max_length=300)
    def_plmn_code = models.CharField(max_length=3, blank=True, null=True)
    tag = models.CharField(max_length=30, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.create_task = datetime.now()
        self.modified_task = datetime.now()
        return super(FR_APIDistributionTask, self).save(*args, **kwargs)

    def __str__(self):
        return f'Creation time: {self.create_task}, message {self.message}, code: {self.def_plmn_code}, tag: {self.tag}'

    class Meta:
        db_table = 'distribution_task'
        verbose_name_plural = 'Distribution Tasks'


MESSAGE_PROCESSING_STATUS = (('created', 'created'),
                             ('in_progress', 'in_progress'),
                             ('done', 'done'),
                             ('failed', 'failed'),
                             )


class FR_APIMessage(models.Model):
    creation_time = models.DateTimeField(blank=False, null=False)

    status = models.CharField(choices=MESSAGE_PROCESSING_STATUS,
                              default='created',
                              max_length=30,
                              blank=False,
                              null=False)

    sending_time = models.DateTimeField(blank=True, null=True)

    distribution_task = models.ForeignKey(FR_APIDistributionTask,
                                          related_name='task',
                                          on_delete=models.PROTECT)

    client = models.ForeignKey(FR_APIClient, blank=False, null=False, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_time = datetime.now()
        return super(FR_APIMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.distribution_task}"

    @property
    def end_task_time(self):
        return self.distribution_task.end_task \
            if self.distribution_task.end_task \
            else datetime(2099, 12, 31, 23, 59, 59)

    class Meta:
        db_table = 'message'
        verbose_name_plural = 'Messages'