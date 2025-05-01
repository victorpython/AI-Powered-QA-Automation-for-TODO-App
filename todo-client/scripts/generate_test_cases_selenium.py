import os
import time
import openai
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Cargar .env y configurar OpenAI
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuración
tool_url = "http://localhost:3000"
output_file = os.path.abspath(os.path.join(__file__, os.pardir, '..', 'docs', 'TEST_CASES.md'))

# Iniciar Chrome headless
tools_opts = Options()
tools_opts.add_argument("--headless")
tools_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=tools_service, options=tools_opts)
time.sleep(1)  # da tiempo a levantar la UI
driver.get(tool_url)
# Cerrar selenium 
driver.quit()

# Definir escenarios de prueba
scenarios = [
    {
        "id": "TC-01",
        "title": "Inicio de sesión válido",
        "precondition": "App en pantalla de Login",
        "steps": ["Visitar Login", "Ingresar credenciales válidas", "Clic en Login"],
        "expected": "Usuario redirigido a lista de tareas y token guardado en localStorage"
    },
    {
        "id": "TC-02",
        "title": "Inicio de sesión inválido",
        "precondition": "App en pantalla de Login",
        "steps": ["Visitar Login", "Ingresar credenciales inválidas", "Clic en Login"],
        "expected": "Mensaje de error y permanece en Login"
    },
    {
        "id": "TC-03",
        "title": "Registro de nuevo usuario",
        "precondition": "App en pantalla de Login",
        "steps": ["Clic en Register", "Ingresar datos de usuario", "Clic en Register"],
        "expected": "Usuario nuevo creado y redirigido a lista de tareas"
    },
    {
        "id": "TC-04",
        "title": "Toggle Dark Mode",
        "precondition": "Usuario autenticado en TodoList",
        "steps": ["Clic en toggle de tema"],
        "expected": "UI cambia entre modo claro y oscuro"
    },
    {
        "id": "TC-05",
        "title": "Cerrar sesión",
        "precondition": "Usuario autenticado en TodoList",
        "steps": ["Clic en botón Logout"],
        "expected": "Redirige a Login y limpia localStorage"
    },
    {
        "id": "TC-06",
        "title": "Persistencia tras recarga",
        "precondition": "Usuario autenticado",
        "steps": ["Recargar la página"],
        "expected": "Permanece en TodoList sin pedir login"
    }
]

# Construir tabla Markdown
table = ["| ID | Título | Precondición | Pasos | Resultado Esperado |", "|---|---|---|---|---|"]
for s in scenarios:
    steps = "; ".join(s["steps"])
    table.append(f"| {s['id']} | {s['title']} | {s['precondition']} | {steps} | {s['expected']} |")

prompt = f"Genera una tabla Markdown con estos casos de prueba:\n" + "\n".join(table)

# Llamar a OpenAI
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