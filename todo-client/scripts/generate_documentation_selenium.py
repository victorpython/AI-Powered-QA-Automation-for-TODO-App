#!/usr/bin/env python3
# scripts/generate_documentation_selenium.py

import os
import time
import openai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Configuración
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key
APP_URL = "http://localhost:3000"  # Ajusta al puerto correcto de tu dev server
OUTPUT = "../docs/TECHNICAL_DOCUMENTATION.md"

# Arranca Chrome en modo headless
opts = Options()
opts.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=opts)
wait = WebDriverWait(driver, 10)

# 1. Explorar Home/Login
driver.get(APP_URL)
time.sleep(1)
home_dom = driver.page_source

# 2. Explorar pantalla de Register
try:
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Register"))).click()
    time.sleep(0.5)
    register_dom = driver.page_source
except Exception:
    register_dom = ""

# 3. Volver a Login y simular Login
driver.get(APP_URL)

# Espera que el label de Username aparezca y obtiene el input asociado
username_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Username')]/following::input[1]"))
)
# Espera que el label de Password aparezca y obtiene el input asociado
password_input = wait.until(
    EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Password')]/following::input[1]"))
)

# Envía las credenciales de prueba
username_input.send_keys("testuser")
password_input.send_keys("testpass")

# Clic en botón Login
login_btn = wait.until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
)
login_btn.click()
time.sleep(1)

# Captura DOM tras login
todo_dom = driver.page_source

driver.quit()

# 4. Preparar prompt para OpenAI
prompt = f"""
He explorado tu frontend React en estas rutas:
- **Home/Login**: {len(home_dom)} caracteres de HTML.
- **Register**: {len(register_dom)} caracteres de HTML.
- **TodoList** (tras login): {len(todo_dom)} caracteres de HTML.

A partir de esta interacción UI, genera DOCUMENTACIÓN TÉCNICA en Markdown que incluya:
- Visión general de la App
- Componentes principales con su propósito
- Estado y props importantes
- Flujo de navegación (login → todos → logout)
- Puntos de extensión posibles
"""

# Llamada a OpenAI utilizando la API v1.0.0+
resp = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un QA especializado en IA."},
        {"role": "user",   "content": prompt}
    ],
    temperature=0.2,
)

# 5. Guardar resultado en archivo Markdown
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(resp.choices[0].message.content.strip())

print(f"✅ {OUTPUT} generado")
