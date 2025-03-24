from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UISession:
    """Класс для тестирования работы UI"""
    UI_URL = "https://teachers.skyeng.ru/schedule"
    LOGIN = "test.tst320@skyeng.ru"
    PASSWORD = "pr4VmfgHsi"
    TITLE = "zxcЙЦУ123 QWEячс @#$"
    DESCRIPTION = "Description 123"

    ADD_BUTTON = (By.CSS_SELECTOR, "ds-icon.add-icon.-size-m")
    PERSONAL_EVENT_OPTION = (By.XPATH, "//span[contains(text(), 'Личное событие')]")
    TITLE_INPUT = (By.CSS_SELECTOR, "input[placeholder*='вебинар']")
    DESCRIPTION_INPUT = (By.CSS_SELECTOR, "textarea[placeholder*='вебинар']")
    SAVE_BUTTON = (By.XPATH, "//button[.//div[@class='text-container' and text()=' Cохранить ']]")
    EDIT_BUTTON = (By.XPATH, "//button[.//div[@class='text-container' and text()=' Редактировать ']]")
    COLOR_GREY = (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(1)")
    COLOR_YELLOW = (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(2)")
    COLOR_GREEN = (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(3)")
    COLOR_PURPLE = (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(4)")
    DELETE_BUTTON = (By.XPATH, "//button[.//div[@class='text-container' and text()=' Удалить ']]")
    CLOSE_BUTTON = (By.CSS_SELECTOR, 'button.close-button')

    def close_popup(self):
        """Закрытие всплывающего баннера"""
        close_btn = WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located(self.CLOSE_BUTTON))
        close_btn.click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located(self.CLOSE_BUTTON))

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.UI_URL)

    def _wait_for_element(self, by, value, timeout=10):
        """Ожидание появления элемента"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def login(self):
        """Авторизация в системе"""
        self._wait_for_element(By.NAME, "username").send_keys(self.LOGIN)
        self._wait_for_element(By.NAME, "password").send_keys(self.PASSWORD)
        self._wait_for_element(By.CSS_SELECTOR, "button.button--primary").click()
        self._wait_for_element(By.CSS_SELECTOR, "body > teachers-cabinet-app svg use")

    def create_event(self, title, description):
        """Создание события"""
        self._wait_for_element(*self.ADD_BUTTON).click()
        self._wait_for_element(*self.PERSONAL_EVENT_OPTION).click()
        self._wait_for_element(*self.TITLE_INPUT).send_keys(title)
        self._wait_for_element(*self.DESCRIPTION_INPUT).send_keys(description)
        self._wait_for_element(*self.SAVE_BUTTON).click()

    def update_event_color(self, event_title):
        """Изменение цвета события"""
        self._wait_for_element(By.XPATH, f"//div[contains(text(), '{event_title}')]").click()
        self._wait_for_element(*self.EDIT_BUTTON).click()
        self._wait_for_element(*self.COLOR_PURPLE).click()
        self._wait_for_element(*self.SAVE_BUTTON).click()

    def update_event_description(self, event_title, new_description):
        """Изменение описания события"""
        self._wait_for_element(By.XPATH, f"//div[contains(text(), '{event_title}')]").click()
        self._wait_for_element(*self.EDIT_BUTTON).click()
        field = self._wait_for_element(*self.DESCRIPTION_INPUT)
        field.clear()
        field.send_keys(new_description)
        self._wait_for_element(*self.SAVE_BUTTON).click()

    def delete_event(self, event_title):
        """Удаление события"""
        self._wait_for_element(By.XPATH, f"//div[contains(text(), '{event_title}')]").click()
        self._wait_for_element(*self.DELETE_BUTTON).click()

    def logout(self):
        """Выход из системы"""
        self._wait_for_element(By.CSS_SELECTOR, "div.button .avatar").click()
        self._wait_for_element(By.CSS_SELECTOR, "a[data-qa-id='btn-logout']").click()
        self._wait_for_element(By.CSS_SELECTOR, "a[href^='https://id.skyeng.ru/login']")

    def close(self):
        """Закрытие браузера"""
        self.driver.quit()