import os
import time
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Carga .env
load_dotenv()
BASE_URL  = os.getenv("APP_URL", "http://localhost:3000")
WAIT_TIME = 10

@pytest.fixture(scope="session")
def driver():
    opts    = Options()
    opts.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    drv     = webdriver.Chrome(service=service, options=opts)
    yield drv
    drv.quit()

@pytest.fixture(autouse=True)
def reset_app(driver):
    # Antes de cada test, vamos al login y limpiamos sesión
    driver.get(BASE_URL)
    yield
    driver.delete_all_cookies()
    driver.execute_script("window.localStorage.clear();")

def unique_username():
    return f"user_{uuid.uuid4().hex[:8]}"

def _find_input_by_label(wait, label_text):
    xpath = f"//label[text()='{label_text}']/following::input[1]"
    return wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

def _find_submit_button(wait, text):
    xpath = f"//button[@type='submit' and normalize-space()='{text}']"
    return wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))

def test_register_and_redirect_to_todos(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    user = unique_username()
    pwd  = "pass1234"

    # Ir a Register
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()=\"Don't have an account? Register\"]"
    ).click()

    # Registrar
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Register").click()

    # Debe aparecer el saludo de TodoList
    welcome = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))
    assert welcome.is_displayed()

def test_login_success(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    user = unique_username()
    pwd  = "pass1234"

    # Paso 0: registro
    driver.get(BASE_URL)
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()=\"Don't have an account? Register\"]"
    ).click()
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Register").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))

    # Paso 1: logout → retorna a Register (no a Login)
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()
    # Esperamos el heading "Register"
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//h1[normalize-space()='Register']"
    )))
    # Cambiar a Login
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()='Already have an account? Login']"
    ).click()
    # Ahora sí, esperamos el heading "Login"
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//h1[normalize-space()='Login']"
    )))

    # Paso 2: login con credenciales válidas
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Login").click()

    # Verificamos que vuelve a TodoList con saludo
    welcome = wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))
    assert welcome.is_displayed()

def test_login_invalid_credentials_shows_error(driver):
    wait = WebDriverWait(driver, WAIT_TIME)

    # Login con datos incorrectos
    _find_input_by_label(wait, "Username").send_keys("wrong")
    _find_input_by_label(wait, "Password").send_keys("wrong")
    _find_submit_button(wait, "Login").click()

    # Localizar por el data-testid que hemos añadido
    err = wait.until(EC.presence_of_element_located((
        By.CSS_SELECTOR, "[data-testid='login-error']"
    )))
    assert err.is_displayed()

def test_toggle_theme_persists(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    user = unique_username()
    pwd  = "pass1234"

    # Registro y llegada a TodoList
    driver.get(BASE_URL)
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()=\"Don't have an account? Register\"]"
    ).click()
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Register").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))

    # Leemos etiqueta del switch antes y después (MUI Switch usa .MuiSwitch-input)
    before_label = driver.find_element(By.CSS_SELECTOR, ".MuiFormControlLabel-label").text
    driver.find_element(By.CSS_SELECTOR, ".MuiSwitch-input").click()
    time.sleep(0.5)
    after_label = driver.find_element(By.CSS_SELECTOR, ".MuiFormControlLabel-label").text
    assert before_label != after_label

    # Persistencia tras recarga
    driver.refresh()
    post_label = driver.find_element(By.CSS_SELECTOR, ".MuiFormControlLabel-label").text
    assert post_label == after_label

def test_logout_clears_session_and_redirects(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    user = unique_username()
    pwd  = "pass1234"

    # Registro + login
    driver.get(BASE_URL)
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()=\"Don't have an account? Register\"]"
    ).click()
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Register").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))

    # Logout → vuelve a Register
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//h1[normalize-space()='Register']"
    )))

    # LocalStorage debe estar vacío
    assert not driver.execute_script("return window.localStorage.getItem('token')")

def test_full_flow(driver):
    wait = WebDriverWait(driver, WAIT_TIME)
    user = unique_username()
    pwd  = "pass1234"

    # Registro + llegada a TodoList
    driver.get(BASE_URL)
    driver.find_element(
        By.XPATH,
        "//button[normalize-space()=\"Don't have an account? Register\"]"
    ).click()
    _find_input_by_label(wait, "Username").send_keys(user)
    _find_input_by_label(wait, "Password").send_keys(pwd)
    _find_submit_button(wait, "Register").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, f"//h1[contains(., 'Welcome, {user}')]"
    )))

    # Toggle tema
    driver.find_element(By.CSS_SELECTOR, ".MuiSwitch-input").click()
    time.sleep(0.3)

    # Logout final → vuelve a Register
    driver.find_element(By.XPATH, "//button[normalize-space()='Logout']").click()
    wait.until(EC.presence_of_element_located((
        By.XPATH, "//h1[normalize-space()='Register']"
    )))
    # Token debe estar borrado
    assert not driver.execute_script("return window.localStorage.getItem('token')")

if __name__ == "__main__":
    pytest.main([__file__, "-q", "--disable-warnings"])
