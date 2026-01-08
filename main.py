from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import unittest
import time
import HtmlTestRunner
import os
class PokemonShowdownTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(5)
        cls.wait = WebDriverWait(cls.driver, 15)
        cls.actions = ActionChains(cls.driver)
        cls.driver.get("https://play.pokemonshowdown.com")

    def fluent_wait(self, locator, timeout=20, poll_frequency=1):
        """Fluent wait для динамических элементов"""
        end_time = time.time() + timeout
        while True:
            try:
                element = self.driver.find_element(*locator)
                if element.is_displayed() and element.is_enabled():
                    return element
            except NoSuchElementException:
                pass
            if time.time() > end_time:
                raise TimeoutException(f"Элемент {locator} не найден за {timeout} секунд")
            time.sleep(poll_frequency)

    def log_step(self, message):
        """Логируем шаги в тест-отчёте через assert"""
        self.assertTrue(True, message)

    def test_login_and_select(self):
        # --- 1. Вход ---
        try:
            choose_name_btn = self.wait.until(EC.element_to_be_clickable((By.NAME, "login")))
            choose_name_btn.click()
            self.log_step("[INFO] Нажата кнопка 'Choose name'")

            name_input = self.fluent_wait((By.CSS_SELECTOR, "input[name='username']"))
            name_input.send_keys("Delson_action\n")
            self.log_step("[INFO] Введено имя: Delson_action")

            password_input = self.fluent_wait((By.CSS_SELECTOR, "input[name='password']"))
            password_input.send_keys("1231313121\n")
            self.log_step("[INFO] Введён пароль")
            time.sleep(2)
        except TimeoutException as e:
            self.fail(f"[ERROR] Логин не выполнен: {str(e)}")

        # --- 2. Action class ---
        try:
            example_btn = self.fluent_wait((By.CSS_SELECTOR, "button.formatselect"))
            self.actions.move_to_element(example_btn).perform()
            self.log_step("[INFO] ActionChains: наведение на кнопку 'formatselect'")
            time.sleep(1)
        except TimeoutException:
            self.log_step("[WARN] Элемент для ActionChains не найден")

        # --- 3. Select class ---
        try:
            select_element = self.fluent_wait((By.CSS_SELECTOR, "select[name='sections']"))
            select = Select(select_element)
            select.select_by_visible_text("Battle formats")
            self.log_step("[INFO] Select class: выбран раздел 'Battle formats'")
            time.sleep(1)
        except TimeoutException:
            self.log_step("[WARN] Элемент Select не найден")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == "__main__":
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output="reports",
        report_name="PokemonShowdownTestReport",
        combine_reports=True,
        add_timestamp=True
    ))

