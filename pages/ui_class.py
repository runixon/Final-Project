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
    COLOR = {
    "grey": (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(1)"),
    "yellow": (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(2)"),
    "green": (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(3)"),
    "purple": (By.CSS_SELECTOR, "div.fx-layout-row.align-items-center > :nth-child(4)")
    }
    CHECK_COLOR = {
    "grey": "rgba(129, 136, 141, 1)",
    "yellow": "rgba(250, 198, 65, 1)",
    "green": "rgba(67, 182, 88, 1)",
    "purple": "rgba(212, 120, 241, 1)"
    }
    DELETE_BUTTON = (By.XPATH, "//button[.//div[@class='text-container' and text()=' Удалить ']]")
    POPUP = (By.CSS_SELECTOR, "div.root.ds-notification-container.notification")
    CLOSE_BUTTON = (By.CSS_SELECTOR, "div.close > button.close-button")

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.UI_URL)

    def _wait_for_element(self, by, value, timeout=5):
        """Ожидание появления элемента"""
        return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))

    def close_popup(self):
        """Закрытие всплывающего баннера"""
        (WebDriverWait(self.driver, 5).until
         (EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-qa-id='popup-background']"))))
        close_btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.CLOSE_BUTTON))
        self.driver.execute_script("arguments[0].click();", close_btn)
        (WebDriverWait(self.driver, 5).until
         (EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.root.ds-notification-container"))))

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
        self._wait_for_element(*self.COLOR["purple"]).click()
        self._wait_for_element(*self.SAVE_BUTTON).click()

    def check_color(self, event_title):
        """Проверка изменения цвета"""
        event = (WebDriverWait(self.driver, 5).until
        (EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'event-block__container')]"
        f"//div[contains(text(), '{event_title}')]/ancestor::div[contains(@class, 'event-block__container')]"))))
        return event.value_of_css_property("border-left-color").lower()

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
        self._wait_for_element(*self.DELETE_BUTTON).click()

    def logout(self):
        """Выход из системы"""
        self._wait_for_element(By.CSS_SELECTOR, "div.button .avatar").click()
        self._wait_for_element(By.CSS_SELECTOR, "a[data-qa-id='btn-logout']").click()

    def close(self):
        """Закрытие браузера"""
        try:
            (WebDriverWait(self.driver, 3).until(EC.any_of(EC.presence_of_element_located
            ((By.XPATH, "//a[contains(@class, 'login') and contains(text(), 'Войти')]")),
            EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 't-btn') and contains(@href, 'login')]")))))
        except Exception:
            pass
        finally:
            self.driver.quit()
