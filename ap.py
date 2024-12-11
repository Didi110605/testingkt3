import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            elif request_type == 'DELETE':
                response = requests.delete(url)
            else:
                raise ValueError(f"Unsupported request type: {request_type}")

            if not expected_error and response.status_code == 200:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        # Logging
        pprint.pprint(f'{request_type} request:')
        pprint.pprint(response.url)
        pprint.pprint(response.status_code)
        pprint.pprint(response.reason)
        try:
            pprint.pprint(response.json())
        except Exception:
            pprint.pprint(response.text)
        pprint.pprint('**********')
        return response

    def get(self, endpoint, endpoint_id=None, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id:
            url += f'/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json()

    def post(self, endpoint, body):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'POST', data=body)
        return response.json()  # Message or full object

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json()


# Базовый URL
BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'
base_request = BaseRequest(BASE_URL_PETSTORE)

# ------- Запросы для сущности user -------
# 1. Создание нового пользователя
user_data = {
    "id": 1,
    "username": "testuser",
    "firstName": "Test",
    "lastName": "User",
    "email": "testuser@example.com",
    "password": "testpassword",
    "phone": "1234567890",
    "userStatus": 1
}
new_user = base_request.post('user', user_data)
pprint.pprint(new_user)

# 2. Получение информации о пользователе
user_info = base_request.get('user', 'testuser')
pprint.pprint(user_info)

# 3. Обновление информации о пользователе
updated_user_data = {
    "id": 1,
    "username": "testuser",
    "firstName": "Updated",
    "lastName": "UserUpdated",
    "email": "updateduser@example.com",
    "password": "updatedpassword",
    "phone": "0987654321",
    "userStatus": 0
}
base_request.post('user', updated_user_data)  # POST для обновления
updated_user_info = base_request.get('user', "testuser")
pprint.pprint(updated_user_info)

# 4. Удаление пользователя
delete_user_response = base_request.delete('user', 'testuser')
pprint.pprint(delete_user_response)

# ------- Запросы для сущности store -------
# 1. Получение данных об инвентаре магазина
inventory = base_request.get('store/inventory')
pprint.pprint(inventory)

# 2. Создание нового заказа
order_data = {
    "id": 1,
    "petId": 1,
    "quantity": 2,
    "shipDate": "2023-10-13T00:00:00.000Z",
    "status": "placed",
    "complete": True
}
new_order = base_request.post('store/order', order_data)
pprint.pprint(new_order)

# 3. Получение информации о заказе по ID заказа
order_id = new_order["id"]
order_info = base_request.get('store/order', order_id)
pprint.pprint(order_info)

# 4. Удаление заказа
delete_order_response = base_request.delete('store/order', order_id)
pprint.pprint(delete_order_response)