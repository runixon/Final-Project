import pytest
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pages.ui_class import UISession


@pytest.fixture(scope="module")
def ui():
    session = UISession()
    session.login()
    yield session


@allure.title("Создание персонального события")
def test_create_event(ui):
    with allure.step("Создание нового персонального события"):
        ui.create_event(ui.TITLE, ui.DESCRIPTION)
        ui.close_popup()

    with allure.step("Проверка отображения события"):
        element = ui._wait_for_element(By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]")
        assert element.is_displayed()


@allure.title("Изменение цвета события")
def test_update_event_color(ui):
    with allure.step("Изменение цвета события (Фиолетовый)"):
        ui.update_event_color(ui.TITLE)
        ui.close_popup()

    with allure.step("Проверка изменения цвета"):
        expected_color = ui.CHECK_COLOR["purple"]
        actual_color = ui.check_color(ui.TITLE)
    assert actual_color == expected_color, f"Цвет {actual_color} не соответствует ожидаемому {expected_color}"


@allure.title("Обновление описания события")
def test_update_event_description(ui):
    with allure.step("Изменение описания события"):
        new_desc = "Updated Description 123"
        ui.update_event_description(ui.TITLE, new_desc)
        ui.close_popup()

    with allure.step("Проверка обновления описания"):
        ui._wait_for_element(By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]").click()
        modal = ui._wait_for_element(By.CSS_SELECTOR, "div.popup")
        description_block = modal.find_element(By.CSS_SELECTOR, "div.description p")
        assert new_desc in description_block.text


@allure.title("Удаление события")
def test_delete_event(ui):
    with allure.step("Удаление события"):
        ui.delete_event(ui.TITLE)
        ui.close_popup()

    with (allure.step("Проверка отсутствия события")):
        WebDriverWait(ui.driver, 5).until
        (EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]")))


@allure.title("Выход из системы")
def test_logout(ui):
    with allure.step("Выполнение выхода"):
        ui.logout()

    with allure.step("Завершение сессии"):
        ui.close()
