import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from testdata.DataProvider import DataProvider

class Authorization:
    def __init__(self, driver: WebDriver) -> None:
        self.__driver = driver

    @allure.step("Авторизация")
    def login_with(self) -> None:
        WebDriverWait(self.__driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//span[@class='header-controls__text']"), "Войти"))
        self.__driver.find_element(By.XPATH, "//*[text()='Войти']").click()
        element = WebDriverWait(self.__driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#tid-input")))
        element.clear()
        element.send_keys(DataProvider().get("phone"))
        WebDriverWait(self.__driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()=' Получить код ']]")))
        self.__driver.find_element(By.XPATH, "//button[.//div[text()=' Получить код ']]").click()
        WebDriverWait(self.__driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//span[@class='header-controls__text']")))

    @allure.step("Проверка авторизации")
    def auth_check(self):
        WebDriverWait(self.__driver, 10).until(
            EC.text_to_be_present_in_element((By.XPATH, "//span[@class='header-controls__text']"), DataProvider().get("username")))
        return self.__driver.find_element(By.XPATH, "//span[@class='header-controls__text']").text