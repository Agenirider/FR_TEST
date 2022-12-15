import logging
import traceback
from datetime import datetime
from email.mime.image import MIMEImage
from threading import Thread

import requests
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from requests.adapters import HTTPAdapter

from fr_sender.settings import API_TOKEN, DEBUG
from sender.models import FR_APIMessage, FR_APIDistributionTask, FR_APIClient

logger = logging.getLogger(__name__)


def send_message(message_object_):
    api_adapter = HTTPAdapter(max_retries=2 if DEBUG else 5)
    session = requests.Session()

    data: dict = {'id': message_object_.id,
                  'phone': f'{message_object_.client.def_plmn_code}{message_object_.client.phone_number}',
                  'text': message_object_.distribution_task.message
                  }

    api_url: str = f'https://probe.fbrq.cloud/v1/send/{message_object_.id}'
    session.mount(api_url, api_adapter)
    headers = {"Content-Type": "application/json", "Authorization": 'Bearer ' + API_TOKEN}
    message_object_.status = 'in_progress'
    message_object_.save()
    message_object_.sending_time = datetime.now()

    try:
        api_response = requests.post(api_url, json=data, headers=headers, timeout=10)
        api_response.raise_for_status()
        message_object_.status = 'done'
        logger.info(f'Message to '
                    f'{message_object_.client.def_plmn_code}{message_object_.client.phone_number} '
                    f'sent')

    except Exception as err:
        message_object_.status = 'failed'
        traceback.print_exc()
        logger.error(f'Task {message_object_.distribution_task.id} '
                     f'Message {message_object_.id}'
                     f'Client {message_object_.client.id}')

    message_object_.save()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def get_new_tasks():
    messages = list(FR_APIMessage.objects.filter(status__in=['created']).select_related('distribution_task',
                                                                                        'client'))

    print(f'NEW MESSAGES------------> {len(messages)}')

    for m in messages:
        start_sending = m.distribution_task.start_task
        end_sending = m.distribution_task.end_task \
            if m.distribution_task.end_task \
            else datetime(2099, 12, 31, 23, 59, 59)

        if start_sending < datetime.now() < end_sending:
            thread = Thread(target=send_message, args=(m,))
            thread.start()


def stat_email_sender(email, context_data, html_template):
    if not DEBUG:
        try:
            content = render_to_string(html_template, context_data)
            msg = EmailMultiAlternatives(subject='TEST TASK STAT',
                                         body=content,
                                         from_email='test@test.com',
                                         to=[email])

            msg.content_subtype = "html"
            msg.send()

        except Exception:
            print(traceback.print_exc())
            logger.error(traceback.print_exc())

    else:
        logger.error('Can`t sending email due DEBUG mode')


@shared_task
def send_statistics():
    stat_result: dict = {}

    tasks = list(FR_APIDistributionTask.objects.all())
    stat_result.update({'total_tasks': len(tasks)})

    messages = FR_APIMessage.objects.filter(distribution_task_id__in=[task.id for task in tasks])
    stat_result.update({'total_messages': len(tasks)})

    clients = list(FR_APIClient.objects.all())
    stat_result.update({'total_clients': len(clients)})

    messages_done: int = len([x for x in messages if x.status == 'done'])
    messages_failed: int = len([x for x in messages if x.status == 'failed'])
    messages_created: int = len([x for x in messages if x.status == 'created'])
    messages_in_progress: int = len([x for x in messages if x.status == 'in_progress'])

    stat_result.update({
        'messages_done': messages_done,
        'messages_failed': messages_failed,
        'messages_created': messages_created,
        'messages_in_progress': messages_in_progress,
    })

    stat_email_sender('boss@test.com', stat_result, 'statistics.html')