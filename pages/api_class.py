import requests
import allure

class APIClass:
    API_URL = "https://api-teachers.skyeng.ru/v2/schedule"
    TOKEN = ("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1c2VySWQiOjE0NzIwMDY5LCJpZGVudGl0eSI6InRlc3QudHN0MzIwQHNreWVuZy5ydSIsImlkZW50aXR5TG9naW4iOm51bGwsImlkZW50aXR5RW1haWwiOiJ0ZXN0LnRzdDMyMEBza3llbmcucnUiLCJpZGVudGl0eVBob25lIjoiKzc5ODU0NTg2NTY4IiwibmFtZSI6InRlc3RURUNUIiwic3VybmFtZSI6bnVsbCwiZW1haWwiOiJ0ZXN0LnRzdDMyMEBza3llbmcucnUiLCJ1aUxhbmd1YWdlIjoicnUiLCJsb2NhbGUiOiJydSIsInNlcnZpY2VMb2NhbGUiOm51bGwsInVhcyI6MzAsImp3dFR5cGUiOjEsImp0aSI6InZYb3ZIbGdxNGw5SE1YWEllNUY5TVNramtkQjRLTHd1IiwiYnJhbmQiOm51bGwsImV4cCI6MTc0MjU0NjM3MiwiYmlydGhkYXkiOiIyMDA3LTEyLTI4IiwiYUlzU3Ryb25nIjp0cnVlLCJhVHlwZSI6IlVTRVJOQU1FX1BBU1NXT1JEIiwiYVRpbWUiOjE3NDI0NTk5NzAsInJvbGVzIjpbIlJPTEVfVEVBQ0hFUl9DQU5ESURBVEUiLCJST0xFX1RFQUNIRVJfQ0FORElEQVRFX0JBU0VfQUNDRVNTIiwiUk9MRV9UUk1fVVBMT0FEX0ZJTEUiLCJST0xFX1RUQ19VU0FHRSIsIlJPTEVfVklNQk9YX1RFQUNIRVJfVVNBR0UiLCJST0xFX1RFQUNIRVIiLCJST0xFX0NSTTJfVEVBQ0hFUl9BQ0NFU1MiLCJST0xFX1RFQUNIRVJTX0NBQklORVRfQkFTRV9BQ0NFU1MiLCJST0xFX01BVEhfVEVBQ0hFUiIsIlJPTEVfTUFUSF9DT05URU5UX1RIRU1FX1ZJRVciXX0.W_69TaCBrGBb1RJ-jb870S7JEqV739WkNoGSCDwvPs0HHjg-DXzUwv4AG8t4_rlwOgF0_l4q2OmDRxwu9nNo8XCani86YfO2PpsaZcKg-jHlZPZ5SmpBoLdD-AYJttpnv2mAwEyytxB-hJGWC0GvwuNwXxxd6apvCzM_zmV2omk7eY-iWIEH9_YO5p85kU_GI-2rSSr68VPmKWmNa1jqa7m0PsXUgcDpX-2JsQ5890be8HSVNgHBK3rW-GGcmk1Z8q7I3pinLJ7fJp9Uh0iOvk_m2ZTnVB3YgNBJyBsicg0v6cK5X4bojhB9I4D4qNrPsdSuDFOaqV7NbC85i5zzU7B7Y72V3x7alZSefRBoU-OFGs7V5jXucni5M4aSP8mrZSv4U10HGjB3uczGMvLEPdlUEHgpnc8_Zgs2F8GJHXdkcGD0ZKG5IwX8GxytfkQkF6_089Z5iLn8Cz7Bm_Vr8YpDMUrbKKN0QMHJgW37XZgebNKnrTfPeItng2smi8qC11L0uzRSQi8YtG8-zZwJncEmktnOKS4_2uZ7WfzfqhOILhH075Yxl3exJZwwg8Mfwxx3DkKG6zunrXISWS4dWoY8-Iv0fiWs2_uRcXXQeXM6wxsGO_6Y8JMLuudb42V08j4_twwKe2uGTF2JJ4kIkbTiT2l48sP3kIDLs9PyEXs")
    START_AT = "2025-03-22T21:00:00+03:00"
    END_AT = "2025-03-22T22:30:00+03:00"
    EVENT_TITLE = "Test Event"
    EVENT_DESCRIPTION = "Test Description"
    COLOR_GREY = "#F4F5F6"
    COLOR_GREEN = "#EBFDF2"
    COLOR_YELLOW = "#FFF7C7"
    COLOR_PURPLE = "#F9EBFF"
    UPDATED_TITLE = "Updated Test Event"
    UPDATED_DESCRIPTION = "Updated Test Description"

    def __init__(self):
        self.base_url = self.API_URL
        self.headers = {
            "Cookie": f"token_global={self.TOKEN}",
            "Content-Type": "application/json"
        }

    @allure.step("Выполнение запроса {method} {url}")
    def _make_request(self, method, url, json=None):
        """Общий метод для выполнения запросов с обработкой ошибок."""
        try:
            response = requests.request(method, url, json=json, headers=self.headers)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}. Response: {response.text}")

    @allure.step("Получение расписания с {from_date} по {till_date}")
    def get_schedule(self, from_date, till_date):
        """Получить расписание"""
        url = f"{self.base_url}/events"
        payload = {"from": from_date, "till": till_date, "onlyTypes": []}
        return self._make_request("POST", url, json=payload)

    @allure.step("Создание персонального события с заголовком {title}")
    def create_personal_event(self, title, start_at, end_at, description=""):
        """Создать персональное событие."""
        url = f"{self.base_url}/createPersonal"
        payload = {
            "backgroundColor": self.COLOR_GREY,
            "color": self.COLOR_GREY,
            "description": description,
            "title": title,
            "startAt": start_at,
            "endAt": end_at
        }
        return self._make_request("POST", url, json=payload)

    @allure.step("Обновление персонального события с ID {event_id}")
    def update_personal_event(self, event_id, title, start_at, end_at, description="", background_color=None):
        """Обновить персональное событие."""
        if background_color is None:
            background_color = self.COLOR_GREY
        url = f"{self.base_url}/updatePersonal"
        payload = {
            "backgroundColor": background_color,
            "color": self.COLOR_GREY,
            "description": description,
            "title": title,
            "startAt": start_at,
            "endAt": end_at,
            "id": event_id,
            "oldStartAt": start_at
        }
        return self._make_request("POST", url, json=payload)

    @allure.step("Удаление персонального события с ID {event_id}")
    def delete_personal_event(self, event_id, start_at):
        """Удалить персональное событие."""
        url = f"{self.base_url}/removePersonal"
        payload = {"id": event_id, "startAt": start_at}
        return self._make_request("POST", url, json=payload)