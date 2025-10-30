import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="module")
def driver():
    options= webdriver.ChromeOptions()
    options.add_argument('--headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

now=time.strftime("%d%m%Y")
names = ['', f'name{now}', f'mail{now}@gmail.com']
mails = ['', f'name{now}', f'mail{now}@gmail.com']
passwords = ['', f'pass{now}', f'mail{now}@gmail.com']
correct = {'name': f'name{now}', 'mail': f'mail{now}@gmail.com', 'password': f'pass{now}'}

test_data = []
for n in names:
    for m in mails:
        for p in passwords:
            if (n, m, p) == (correct['name'], correct['mail'], correct['password']):
                continue
            expected = (
                n != correct['name'],
                m != correct['mail'],
                p != correct['password']
            )
            test_data.append((n, m, p, expected))

@pytest.fixture(scope="function")
def open_registration_page(driver, wait):
    driver.delete_all_cookies()

    driver.get('https://ek.ua/ua/')
    
    LOGIN_BTN = (By.XPATH, "//span[contains(@class, 'wu_entr') and contains(@class, 'h')]")
    REG_BTN = (By.XPATH, "//button[contains(@class, 'signin-with') and contains(@class, 'signin-with-reg')]")

    wait.until(EC.element_to_be_clickable(LOGIN_BTN)).click()
    wait.until(EC.element_to_be_clickable(REG_BTN)).click()
    
    yield driver 

    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();") 
    driver.execute_script("window.sessionStorage.clear();")
    driver.refresh()




class TestRegistration():
    @pytest.mark.parametrize("name, mail, password, expected_errors", test_data)
    def test_negative_registration(self, open_registration_page, wait, name, mail, password, expected_errors):
        driver = open_registration_page 

        NAME_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[3]")
        MAIL_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[4]")
        PASSWORD_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[5]")
        FINISH_REG_BTN = (By.XPATH, "(//button[contains(@class, 'ek-form-btn') and contains(@class, ' blue')])[2]")

        ERROR_LOCATORS = [
            (By.XPATH, '//div[contains(@class, "ek-form-text") and contains(., "Ім\'я")]'),
            (By.XPATH, '//div[contains(@class, "ek-form-text") and (contains(., "email") or contains(., "e-mail"))]'),
            (By.XPATH, '//div[contains(@class, "ek-form-text") and contains(., "Пароль")]')
        ]

        name_input = wait.until(EC.visibility_of_element_located(NAME_INPUT))
        mail_input = wait.until(EC.visibility_of_element_located(MAIL_INPUT))
        password_input = wait.until(EC.visibility_of_element_located(PASSWORD_INPUT))
        fin_btn = wait.until(EC.element_to_be_clickable(FINISH_REG_BTN))

        name_input.clear()
        name_input.send_keys(name)
        mail_input.clear()
        mail_input.send_keys(mail)
        password_input.clear()
        password_input.send_keys(password)
        fin_btn.click()

        visible = []
        for loc in ERROR_LOCATORS:
            try:
                elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located(loc))
                visible.append(elem.is_displayed())
            except:
                visible.append(False)

        assert tuple(visible) == expected_errors, f"Expected {expected_errors}, got {visible} for {name}, {mail}, {password}"

    @pytest.mark.parametrize("name, mail, password", [(f'corname{now}',f'cormail{now}@gmail.com',f'corpass{now}')])
    def test_positive_registration(self,open_registration_page, wait, name, mail, password):
        driver = open_registration_page 
    
        NAME_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[3]")
        MAIL_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[4]")
        PASSWORD_INPUT = (By.XPATH, "(//input[@class='ek-form-control'])[5]")
        FINISH_REG_BTN = (By.XPATH, "(//button[contains(@class, 'ek-form-btn') and contains(@class, ' blue')])[2]")

        SUCCESS_LOCATOR=('xpath',"//div[@class='modal-header']")

        name_input = wait.until(EC.visibility_of_element_located(NAME_INPUT))
        mail_input = wait.until(EC.visibility_of_element_located(MAIL_INPUT))
        password_input = wait.until(EC.visibility_of_element_located(PASSWORD_INPUT))
        fin_btn = wait.until(EC.element_to_be_clickable(FINISH_REG_BTN))
    
        name_input.clear()
        name_input.send_keys(name)
        mail_input.clear()
        mail_input.send_keys(mail)
        password_input.clear()
        password_input.send_keys(password)
        fin_btn.click()

        assert EC.visibility_of_element_located(SUCCESS_LOCATOR)
