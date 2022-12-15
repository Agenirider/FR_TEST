from django.urls import path

from . import views

urlpatterns = [
    path('get_clients',
         views.get_clients),
    path('get_client/<int:client_id>',
         views.get_client),
    path('create_client',
         views.create_client),
    path('delete_client/<int:client_id>',
         views.delete_client),
    path('update_client/<int:client_id>',
         views.update_client),
    path('get_distribution_tasks',
         views.get_distribution_tasks),
    path('get_distribution_task/<int:task_id>',
         views.get_distribution_task),
    path('create_distribution_task',
         views.create_distribution_task),
    path('update_distribution_task/<int:task_id>',
         views.update_distribution_task),
    path('delete_distribution_task/<int:task_id>',
         views.delete_distribution_task),
    path('get_task_result/<int:task_id>',
         views.get_task_result),
    path('get_stat',
         views.get_stat),
]
