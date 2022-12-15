from django.db.models import Q
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from sender.models import (FR_APIClient,
                           FR_APIDistributionTask,
                           FR_APIMessage)

from sender.serializers import (FR_API_CLIENT_SERIALIZER,
                                FR_API_TASK_SERIALIZER)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_clients(request) -> Response:
    clients: list = list(FR_APIClient.objects.all())
    unpacked_clients: list = [model_to_dict(c) for c in clients]
    return Response(unpacked_clients, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_client(request, client_id):
    try:
        client = FR_APIClient.objects.get(pk=client_id)
        return Response(model_to_dict(client),
                        status=status.HTTP_200_OK)

    except FR_APIClient.DoesNotExist:
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_client(request):
    serializer = FR_API_CLIENT_SERIALIZER(data=request.data)
    serializer.is_valid(raise_exception=True)
    err = serializer.errors

    if err:
        return Response({'error': f'wrong parameters: {err}'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serialized_data = serializer.data

        FR_APIClient.objects.create(phone_number=serialized_data.get('phone_number'),
                                    def_plmn_code=serialized_data.get('def_plmn_code'),
                                    tag=serialized_data.get('tag'),
                                    time_zone=serialized_data.get('time_zone')
                                    )

        return Response(status=status.HTTP_200_OK)

    return Response({'error': 'request not valid'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([AllowAny, ])
def delete_client(request, client_id):
    try:
        client = FR_APIClient.objects.get(pk=client_id)
        client.delete()
        return Response(status=status.HTTP_200_OK)

    except FR_APIClient.DoesNotExist:
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def update_client(request, client_id):
    exist_client = FR_APIClient.objects.filter(pk=client_id)

    if not exist_client.exists():
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = FR_API_CLIENT_SERIALIZER(data=request.data)
    serializer.is_valid(raise_exception=True)
    err = serializer.errors

    if err:
        return Response({'error': f'wrong parameters: {err}'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        d = dict(serializer.data)
        serialized_data = {key: val for key, val in d.items() if val}
        exist_client.update(**serialized_data)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_distribution_tasks(request):
    tasks: list = list(FR_APIDistributionTask.objects.all())
    unpacked_tasks: list = [model_to_dict(t) for t in tasks]
    return Response(unpacked_tasks, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_distribution_task(request, task_id):
    try:
        task = FR_APIDistributionTask.objects.get(pk=task_id)
        return Response(model_to_dict(task),
                        status=status.HTTP_200_OK)

    except FR_APIDistributionTask.DoesNotExist:
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def create_distribution_task(request):
    serializer = FR_API_TASK_SERIALIZER(data=request.data)
    serializer.is_valid(raise_exception=True)
    err = serializer.errors

    if err:
        return Response({'error': f'wrong parameters: {err}'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        serialized_data = serializer.data

        tag: str = serialized_data.get('tag')
        def_plmn_code: str = serialized_data.get('def_plmn_code')

        task = FR_APIDistributionTask.objects.create(message=serialized_data.get('message'),
                                                     start_task=serialized_data.get('start_task'),
                                                     tag=tag,
                                                     def_plmn_code=def_plmn_code
                                                     )

        clients = list(FR_APIClient.objects.filter(Q(tag=tag)
                                                   | Q(def_plmn_code=def_plmn_code)
                                                   | Q(tag=tag, def_plmn_code=def_plmn_code)))

        if clients:
            for c in clients:
                FR_APIMessage.objects.create(status='created',
                                             distribution_task=task,
                                             client=c)
        else:
            return Response({'error': 'unknown tag or def_plmn_code'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    return Response({'error': 'request not valid'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def update_distribution_task(request, task_id):
    exist_client = FR_APIDistributionTask.objects.filter(pk=task_id)

    if not exist_client.exists():
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)

    serializer = FR_API_TASK_SERIALIZER(data=request.data)
    serializer.is_valid(raise_exception=True)
    err = serializer.errors

    if err:
        return Response({'error': f'wrong parameters: {err}'}, status=status.HTTP_400_BAD_REQUEST)

    if serializer.is_valid():
        d = dict(serializer.data)
        serialized_data = {key: val for key, val in d.items() if val}
        exist_client.update(**serialized_data)
        return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([AllowAny, ])
def delete_distribution_task(request, task_id):
    try:
        task = FR_APIDistributionTask.objects.get(pk=task_id)
        task.delete()
        return Response(status=status.HTTP_200_OK)

    except FR_APIDistributionTask.DoesNotExist:
        return Response({'error': 'client does not exist'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_task_result(request, task_id):
    task = FR_APIDistributionTask.objects.get(pk=task_id)
    messages: list = list(FR_APIMessage.objects.filter(distribution_task=task))

    messages_done: int = len([x for x in messages if x.status == 'done'])
    messages_failed: int = len([x for x in messages if x.status == 'failed'])
    messages_created: int = len([x for x in messages if x.status == 'created'])
    messages_in_progress: int = len([x for x in messages if x.status == 'in_progress'])

    return Response({'task': task.id,
                     'tag': task.tag,
                     'messages_done': messages_done,
                     'messages_failed': messages_failed,
                     'messages_created': messages_created,
                     'messages_in_progress': messages_in_progress,
                     'clients': [c.client_id for c in messages]
                     },
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_stat(request):
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

    return Response(stat_result, status=status.HTTP_200_OK)
