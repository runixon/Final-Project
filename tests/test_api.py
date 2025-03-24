import pytest
import allure
from pages.api_class import APIClass

@pytest.fixture(scope="module")
def api_client():
    return APIClass()

@pytest.fixture(scope="module")
def created_event(api_client):
    with allure.step("Создание тестового события"):
        response = api_client.create_personal_event(
            api_client.EVENT_TITLE,
            api_client.START_AT,
            api_client.END_AT
        )
        assert response.status_code == 200, "Failed to create event"
        event_data = response.json()["data"]["payload"]
        yield {
            "id": event_data["id"],
            "start_at": api_client.START_AT
        }
    with allure.step("Удаление тестового события"):
        api_client.delete_personal_event(event_data["id"], api_client.START_AT)

@allure.step("Получение расписания")
def test_get_schedule(api_client):
    response = api_client.get_schedule(api_client.START_AT, api_client.END_AT)
    assert response.status_code == 200
    assert "events" in response.json()["data"]

@allure.step("Создание персонального события")
def test_create_personal_event(api_client):
    response = api_client.create_personal_event(
        api_client.EVENT_TITLE,
        api_client.START_AT,
        api_client.END_AT
    )
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    event_data = response.json()["data"]["payload"]
    assert "id" in event_data, "Ключ 'id' отсутствует в ответе"

    inner_payload = event_data["payload"]
    assert "title" in inner_payload, "Ключ 'title' отсутствует в ответе"
    assert inner_payload["title"] == api_client.EVENT_TITLE, "Название события не совпадает"

@allure.step("Изменение цвета фона события")
def test_update_event_background_color(api_client, created_event):
    update_response = api_client.update_personal_event(
        created_event["id"],
        api_client.EVENT_TITLE,
        api_client.START_AT,
        api_client.END_AT,
        description="",
        background_color=api_client.COLOR_PURPLE
    )
    assert update_response.status_code == 200
    response_data = update_response.json()
    assert response_data["data"]["payload"]["payload"]["backgroundColor"] == api_client.COLOR_PURPLE

@allure.step("Изменение описания события")
def test_update_event_description(api_client, created_event):
    update_response = api_client.update_personal_event(
        created_event["id"],
        api_client.EVENT_TITLE,
        api_client.START_AT,
        api_client.END_AT,
        description=api_client.UPDATED_DESCRIPTION
    )
    assert update_response.status_code == 200
    response_data = update_response.json()
    assert response_data["data"]["payload"]["payload"]["description"] == api_client.UPDATED_DESCRIPTION

@allure.step("Удаление события")
def test_delete_personal_event(api_client, created_event):
    delete_response = api_client.delete_personal_event(created_event["id"], api_client.START_AT)
    assert delete_response.status_code == 200
    assert delete_response.json()["data"] == True