from pages.MainPage import MainPage
from pages.Authorization import Authorization
from testdata.DataProvider import DataProvider
import time

def test_go_main_page(browser):
    main_page = MainPage(browser)
    authorization = Authorization(browser)
    main_page.go_main_page()
    authorization.login_with()

    assert authorization.auth_check() == DataProvider().get("username")
    
    # time.sleep(10)