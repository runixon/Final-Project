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
    session.close()


@allure.title("Создание персонального события")
def test_create_event(ui):
    with allure.step("Создание нового персонального события"):
        ui.create_event(ui.TITLE, ui.DESCRIPTION)
        ui.close_popup()  # Закрываем всплывающее окно

    with allure.step("Проверка отображения события"):
        element = ui._wait_for_element(By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]")
        assert element.is_displayed()


@allure.title("Изменение цвета события")
def test_update_event_color(ui):
    with allure.step("Изменение цвета события (Фиолетовый)"):
        ui.update_event_color(ui.TITLE)
        ui.close_popup()
    with allure.step("Проверка применения цвета"):
        selected_element = ui.driver.find_element(*ui.COLOR_PURPLE)
        assert "color-circle__border" in selected_element.get_attribute("class")


@allure.title("Обновление описания события")
def test_update_event_description(ui):
    with allure.step("Изменение описания события"):
        new_desc = "Updated Description 123"
        ui.update_event_description(ui.TITLE, new_desc)
        ui.close_popup()
    with allure.step("Проверка обновления описание"):
        ui._wait_for_element(By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]").click()
        modal = ui._wait_for_element(By.CSS_SELECTOR, "div.popup")
        description_block = modal.find_element(By.CSS_SELECTOR, "div.description p")
        assert new_desc in description_block.text


@allure.title("Удаление события")
def test_delete_event(ui):
    with allure.step("Удаление события"):
        ui.delete_event(ui.TITLE)
    with allure.step("Проверка отсутствия события"):
        WebDriverWait(ui.driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{ui.TITLE}')]")))


@allure.title("Выход из системы")
def test_logout(ui):
    with allure.step("Выполнение выхода из аккаунта"):
        ui.logout()
    with allure.step("Проверка перехода на страницу авторизации"):
        ui._wait_for_element(By.CSS_SELECTOR, "a[href^='https://id.skyeng.ru/login']")