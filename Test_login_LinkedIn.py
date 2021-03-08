import pytest
from selenium import webdriver
import allure


@pytest.fixture()
def test_setup():
    global driver
    driver = webdriver.Chrome(executable_path="C:\\Users\\Adrian\\.wdm\\drivers\\chromedriver\\win32\\88.0.4324.96\\chromedriver.exe")
    driver.implicitly_wait(10)
    driver.maximize_window()
    yield
    driver.quit()


@allure.description("Validate LinkedIn with valid credentials")
@allure.severity(severity_level="CRITICAL")
def test_validLogin(test_setup):
    driver.get("https://www.linkedin.com/login/pl?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    enter_username("robottest@wp.pl")
    enter_password("robottest12345")
    log("Clicking Login Button")
    driver.find_element_by_xpath("//button[@data-litms-control-urn='login-submit']").click()
    assert "feed" in driver.current_url


@allure.description("Validate LinkedIn with invalid credentials")
@allure.severity(severity_level="NORMAL")
def test_invalidLogin(test_setup):
    driver.get("https://www.linkedin.com/login/pl?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    driver.find_element_by_id("username").clear()
    driver.find_element_by_id("password").clear()
    enter_username("robottest@wp.pl")
    enter_password("robottest12345")
    log("Clicking login button")
    driver.find_element_by_xpath("//button[@data-litms-control-urn='login-submit']").click()
    try:
        assert "feed" in driver.current_url
        log(driver.current_url)
    finally:
        if AssertionError:
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invalid Credentials",
                          attachment_type=allure.attachment_type.PNG)


@allure.step("Entering Username as {0}")
def enter_username(username):
    driver.find_element_by_id("username").send_keys(username)


@allure.step("Entering Password as {0}")
def enter_password(password):
    driver.find_element_by_id("password").send_keys(password)


@allure.step("{0}")
def log(message):
    print(message)