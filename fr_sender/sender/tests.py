import json
from django.test import TestCase
from django.test import tag
from rest_framework.test import APIClient
from deepdiff import DeepDiff

from sender.models import (FR_APIClient,
                           FR_APIMessage,
                           FR_APIDistributionTask)

user_credentials = {'email': 'test_user@testcom',
                    'password': 'SS498JL1Q'}

API_Client = APIClient()


class APITestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        new_client, new_client_is_created = FR_APIClient.objects.get_or_create(phone_number='79121112222')

        new_task, new_task_is_created = FR_APIDistributionTask.objects.get_or_create(message='test message')

        # new_message, new_message_is_created = FR_APIMessage.objects.get_or_create(phone_number='79121112222')

    @tag('client')
    def test_case_1_get_clients(self):
        url = '/api/v1/get_clients'
        response = API_Client.get(url)
        decoded_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_result = [{'id': 1,
                            'phone_number': '1112222',
                            'def_plmn_code': '912',
                            'tag': None,
                            'time_zone': 'UTC'}]

        assert not DeepDiff(decoded_response,
                            expected_result,
                            ignore_order=True)

    @tag('client')
    def test_case_2_get_client(self):
        url = '/api/v1/get_client/1'
        response = API_Client.get(url)
        decoded_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)

        expected_result = {'id': 1,
                           'phone_number': '1112222',
                           'def_plmn_code': '912',
                           'tag': None,
                           'time_zone': 'UTC'}

        assert not DeepDiff(decoded_response,
                            expected_result,
                            ignore_order=True)

    @tag('client')
    def test_case_3_create_client_full_data(self):
        url = '/api/v1/create_client'
        params = {'phone_number': '79129998888',
                  'def_plmn_code': '912',
                  'tag': '#TEST_TAG',
                  'time_zone': 'UTC'}

        response = API_Client.post(url, params, format='json')
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_case_4_create_client_short_data(self):
        url = '/api/v1/create_client'
        params = {'phone_number': '79129998888'}

        response = API_Client.post(url, params, format='json')
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_case_5_create_client_wrong_data(self):
        url = '/api/v1/create_client'
        params = {'phone_number': '9998888'}

        response = API_Client.post(url, params, format='json')
        decoded_response = json.loads(response.content)
        expected_response = {'phone_number': ['Ensure this field has at least 10 characters.']}

        self.assertEqual(response.status_code, 400)

        assert not DeepDiff(decoded_response,
                            expected_response,
                            ignore_order=True)

    @tag('client')
    def test_case_6_delete_client(self):
        new_client, __ = FR_APIClient.objects.get_or_create(phone_number='79121112222')

        url = f'/api/v1/delete_client/{new_client.id}'

        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 200)

    @tag('client')
    def test_case_7_delete_client_wrong_id(self):
        url = '/api/v1/delete_client/100'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_case_8_delete_client_wrong_id_case_2(self):
        url = '/api/v1/delete_client/a'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 404)

    @tag('client')
    def test_case_9_update_client(self):
        new_client, __ = FR_APIClient.objects.get_or_create(phone_number='78881112222')
        url = f'/api/v1/update_client/{new_client.id}'
        params = {'tag': 'NEW TEST TAG'}

        response = API_Client.post(url, params, format='json')
        self.assertEqual(response.status_code, 200)

        cl = FR_APIClient.objects.get(pk=new_client.id)

        assert cl.tag == 'NEW TEST TAG'

    @tag('client')
    def test_case_10_update_client_wrong_id(self):
        url = '/api/v1/delete_client/100'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 400)

    @tag('client')
    def test_case_11_update_client_wrong_id_case_2(self):
        url = '/api/v1/delete_client/aaa'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 404)

    @tag('distribution')
    def test_case_12_get_distribution_tasks(self):
        url = '/api/v1/get_distribution_tasks'
        response = API_Client.get(url)
        decoded_response = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        assert len(decoded_response)

    @tag('distribution')
    def test_case_13_get_distribution_task(self):
        task = FR_APIDistributionTask.objects.get(pk=1)
        url = f'/api/v1/get_distribution_task/{task.id}'
        response = API_Client.get(url)
        decoded_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        assert len(decoded_response)

    @tag('distribution')
    def test_case_14_create_distribution_task(self):
        url = '/api/v1/create_distribution_task'
        params = {'message': 'test_task'}
        response = API_Client.post(url, params, format='json')
        self.assertEqual(response.status_code, 200)

    @tag('distribution')
    def test_case_15_update_distribution_task(self):
        url = '/api/v1/update_distribution_task/1'

        params = {'message': 'test_task_1',
                  'start_task': '2022-12-31T10:10:10'}

        response = API_Client.post(url, params, format='json')
        self.assertEqual(response.status_code, 200)

    @tag('distribution')
    def test_case_16_delete_distribution_task(self):
        new_task, __ = FR_APIDistributionTask.objects.get_or_create(message='--------------TEST------------')

        url = f'/api/v1/delete_distribution_task/{new_task.id}'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 200)

    @tag('distribution')
    def test_case_16_delete_distribution_task_wrong_id(self):
        url = '/api/v1/delete_distribution_task/10000'
        response = API_Client.delete(url)
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        pass
