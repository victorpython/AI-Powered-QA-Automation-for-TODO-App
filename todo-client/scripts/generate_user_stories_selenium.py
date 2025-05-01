import os
import time
import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargar .env y configurar OpenAI
dotenv_path = os.path.abspath(os.path.join(__file__, os.pardir, '..', '.env'))
load_dotenv(dotenv_path)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración de Selenium y URLs
tool_url = "http://localhost:3000"
output_file = os.path.abspath(os.path.join(__file__, os.pardir, '..', 'docs', 'USER_STORIES.md'))

# Iniciar Chrome headless
tools_opts = Options()
tools_opts.add_argument("--headless")
tools_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=tools_service, options=tools_opts)
wait = WebDriverWait(driver, 10)
flows = []

# Registro de usuario
try:
    driver.get(tool_url)
    wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Register"))).click()
    # Captura flujo
    flows.append("Registro de usuario: Visitar pantalla Register → ingresar nuevo usuario y contraseña → clic en Register → redirigir a TodoList")
except:
    flows.append("Registro de usuario: no disponible (Register link no encontrado)")

# Inicio de sesión válido
driver.get(tool_url)
try:
    # encuentra campos y simula login
    username = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Username')]/following::input[1]")))
    password = wait.until(EC.presence_of_element_located((By.XPATH, "//label[contains(text(),'Password')]/following::input[1]")))
    username.send_keys("testuser")
    password.send_keys("testpass")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(1)
    flows.append("Inicio de sesión válido: Ingresar credenciales válidas → clic en Login → ver lista de tareas")
except:
    flows.append("Inicio de sesión válido: falló (Login no encontrado)")

# Alternar tema
try:
    # Asume que existe un switch o botón para tema
    toggle = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='checkbox']")))
    toggle.click()
    flows.append("Alternar tema: Clic en toggle de tema → UI cambia entre claro/oscuro")
except:
    flows.append("Alternar tema: switch no encontrado")

# Cerrar sesión
driver.get(tool_url)
try:
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Logout') or contains(text(),'Sign out')]") ))
    logout_btn.click()
    flows.append("Cerrar sesión: Clic en Logout → redirigir a Login")
except:
    flows.append("Cerrar sesión: boton Logout no encontrado")

# Finalizar Selenium
driver.quit()

# Preparar prompt
tasks_list = "\n".join(f"- {f}" for f in flows)
prompt = f"""
A partir de estos flujos de usuario extraídos de la UI:
{tasks_list}

Genera HISTORIAS DE USUARIO en Markdown con formato:
US-XX: Como <rol> quiero <acción> para <beneficio>.
Al menos 6 historias.
"""

# Llamada a OpenAI
resp = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Eres un QA especializado en IA."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.3,
)

# Guardar el resultado
os.makedirs(os.path.dirname(output_file), exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write(resp.choices[0].message.content)

print(f"✅ {output_file} generado")