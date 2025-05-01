import re
from pathlib import Path

# Ruta al Markdown de casos
MD_PATH = Path("prompt_engineering/responses/testcases_response.md")

# Ruta de salida del pytest generado
OUT_PATH = Path("tests/test_api_generated.py")

# Base URL de la API
BASE = "http://localhost:5141"  

# ———————————————————————————————————————————
# Leer y filtrar líneas de la tabla
text = MD_PATH.read_text(encoding="utf-8")
lines = []
for ln in text.splitlines():
    ln = ln.strip()
    if ln.startswith("|") and not re.match(r"\|\s*-+", ln):
        lines.append(ln)

# La primera línea es el header:
header = [h.strip() for h in lines[0].split("|")[1:-1]]
rows   = lines[2:]   # saltamos header + separador

# ———————————————————————————————————————————
# Iniciar un template de Python para pytest
out = [
    "import requests",
    "import pytest",
    "",
    f'BASE = "{BASE}"',
    "",
]

# ———————————————————————————————————————————
# Para cada fila, extraer las columnas y generar la función
for row in rows:
    cols = [c.strip() for c in row.split("|")[1:-1]]
    # Mapeo col_header -> valor
    data = dict(zip(header, cols))

    # Nombre de la función pytest
    name = data["Nombre del caso"]
    fn   = "test_" + re.sub(r"[^\w]+", "_", name.lower()).strip("_")

    endpoint = data["Endpoint"]
    method   = data["Método HTTP"].lower()
    status   = data["Estatus esperado"].split()[0]  # toma solo el número

    # Payload válido: si la columna "Entradas válidas" no es "-" 
    valid = data["Entradas válidas"]
    has_payload = valid not in ("-", "")

    # Escritura de la función
    out.append(f"def {fn}():")
    out.append(f"    \"\"\"{name}\"\"\"")
    out.append(f"    url = BASE + f\"{endpoint}\"")

    if has_payload:
        # Se asume JSON inline separado por comas
        out.append(f"    # TODO: define payload válido como dict Python")
        out.append(f"    payload = {{}}  # << insertar los campos desde testcases_response.md")
        out.append(f"    r = requests.{method}(url, json=payload)")
    else:
        out.append(f"    r = requests.{method}(url)")

    out.append(f"    assert r.status_code == {status}, f\"Status inesperado: {{r.status_code}}\"")

    # Validaciones: comparar JSON si aplica
    if method in ("get", "post", "put", "delete"):
        out.append(f"    data = r.json()")
        out.append(f"    assert data is not None")
    out.append("")  # Línea en blanco

# ———————————————————————————————————————————
# Grabar el archivo
OUT_PATH.write_text("\n".join(out), encoding="utf-8")
print(f"✅ Tests generados en {OUT_PATH}")
