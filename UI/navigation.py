import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Navigation:

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализирует страницу с предоставленным веб-драйвером.

        :param driver: WebDriver: Экземпляр веб-драйвера для управления браузером.
        """
        self.__driver = driver

    @allure.step("Переход на главную страницу магазина")
    def go_main(self) -> None:
        """
        Перенаправляет пользователя на главную страницу магазина.

        Примечание: Не работает, если использовать на главной странице.
        """
        with allure.step("Клик на логотип для перехода на главную страницу"):
            self.__driver.find_element(
                By.XPATH, "//span[@class='header__logo-wrapper']").click()

        with allure.step("Ожидание отображения баннера с акциями"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='main-page__banners']"))
            )
        return self.__driver.current_url

    @allure.step("Переход в личный профиль")
    def go_profile(self) -> None:
        """
        Перенаправляет пользователя в личный профиль для доступа к личным данным и настройкам.

        Примечание: Требуется авторизация.
        """
        with allure.step("Клик на иконку профиля для перехода в личный профиль"):
            self.__driver.find_element(
                By.CSS_SELECTOR,
                "button.header-controls__btn[aria-label='Меню профиля']").click()

        with allure.step("Ожидание отображения заголовка профиля"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h2[@class='profile-page__title']"))
            )
        return self.__driver.current_url

    @allure.step("Переход в заказы")
    def go_orders(self) -> None:
        """
        Перенаправляет пользователя в раздел заказов для просмотра истории покупок и статусов текущих заказов.

        Примечание: Требуется авторизация.
        """
        with allure.step("Клик на иконку заказов для перехода в раздел заказов"):
            self.__driver.find_element(
                By.CSS_SELECTOR,
                "button.header-controls__btn.header-controls__btn--mh[aria-label='Заказы']").click()

        with allure.step("Ожидание отображения заголовка заказов"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h2[@class='profile-orders-page__title']"))
            )
        return self.__driver.current_url

    @allure.step("Переход в закладки")
    def go_bookmarks(self) -> None:
        """
        Перенаправляет пользователя в раздел закладок для просмотра добавленных товаров и отслеживания подписок.

        Примечание: Требуется авторизация.
        """
        with allure.step("Клик на иконку закладок для перехода в закладки"):
            self.__driver.find_element(
                By.CSS_SELECTOR,
                "button.header-controls__btn[aria-label='Закладки']").click()

        with allure.step("Ожидание отображения заголовка закладок"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h1[@class='bookmarks-page__title']"))
            )
        return self.__driver.current_url

    @allure.step("Переход в корзину")
    def go_cart(self) -> None:
        """Перенаправляет пользователя в корзину для просмотра добавленных товаров и оформления заказов."""
        with allure.step("Клик на иконку корзины для перехода в корзину"):
            self.__driver.find_element(
                By.CSS_SELECTOR,
                "button.header-controls__btn[aria-label='Корзина']").click()

        with allure.step("Ожидание отображения заголовка корзины"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h1[@class='cart-page__title']"))
            )
        return self.__driver.current_url

    def go_main(self) -> None:
        """Перенаправляет пользователя на главную страницу магазина."""
        with allure.step("Клик на логотип для перехода на главную страницу"):
            self.__driver.find_element(
                By.XPATH, "//span[@class='header__logo-wrapper']").click()

        with allure.step("Ожидание отображения баннера с акциями"):
            WebDriverWait(self.__driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='main-page__banners']"))
            )
        return self.__driver.current_url

    @allure.step("Попытка перехода в {section} без авторизации")
    def go_section_unauth(self, section: str) -> bool:
        """
        Метод производит попытку перенаправить пользователя в указанный раздел, требующий авторизации.

        :returns: bool: True если модальное окно аутентификации отобразилось, иначе False.
        """
        with allure.step(f"Клик на иконку {section} для проверки отображения модального окна аутентификации"):
            try:
                if section == "profile":
                    self.__driver.find_element(
                        By.CSS_SELECTOR,
                        "button.header-controls__btn[aria-label='Меню профиля']").click()
                elif section == "orders":
                    self.__driver.find_element(
                        By.CSS_SELECTOR,
                        "button.header-controls__btn.header-controls__btn--mh[aria-label='Заказы']").click()
                elif section == "bookmarks":
                    self.__driver.find_element(
                        By.CSS_SELECTOR, "button.header-controls__btn[aria-label='Закладки']").click()

                with allure.step("Ожидание отображения модального окна аутентификации"):
                    modal_element = WebDriverWait(
                        self.__driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, "//p[@class='auth-modal-content__text']")))
                return True if modal_element.is_displayed() else False

            except TimeoutException:
                return False
