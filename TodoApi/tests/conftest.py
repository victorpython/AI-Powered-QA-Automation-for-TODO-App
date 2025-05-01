import pytest
import requests

BASE = "http://localhost:5141"   

@pytest.fixture(scope="session")
def auth_headers():
    """
    1) Intentar login; si no es 200, registrar el usuario
    2) Volver a hacer login
    3) Extraer el JWT y devolver el header
    """
    login_url    = f"{BASE}/api/Auth/login"
    register_url = f"{BASE}/api/Auth/register"

    credentials = {
        "username": "testuser",     # coincide con AuthRequest.Username
        "password": "Test123!"      # coincide con AuthRequest.Password
    }

    # 1) Intento de login
    resp = requests.post(login_url, json=credentials)

    # 2) Si no es 200 (400, 401, 404… lo que sea), intentamos registrar
    if resp.status_code != 200:
        reg = requests.post(register_url, json=credentials)
        # consideramos válido tanto 201 Created como 200 OK (o incluso 400 si ya existe)
        assert reg.status_code in (200, 201, 400), f"Fallo al registrar: {reg.status_code} {reg.text}"
        # 2b) ahora sí volvemos a login
        resp = requests.post(login_url, json=credentials)

    # 3) Debe ser 200
    assert resp.status_code == 200, f"No pudimos autenticarnos: {resp.status_code} {resp.text}"
    body = resp.json()

    # El AuthResponse devuelve .Token (o .Username, pero interesa el token)
    token = body.get("token") or body.get("accessToken")
    assert token, "El login no devolvió un JWT"

    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="session")
def initial_todo(auth_headers):
    """
    Publicar una tarea Todo para que GET/PUT/DELETE tengan algo sobre lo que operar
    Devuelve el nuevo ID del entero de Todo
    """
    url     = f"{BASE}/api/Todo"
    payload = {
        "Title":       "Fixture: tarea inicial",
        "IsCompleted": False,
        "Category":    "Work"
    }

    resp = requests.post(url, json=payload, headers=auth_headers)
    # Debe ser un 201 creado
    assert resp.status_code == 201, f"Falló la creación inicial: {resp.status_code} {resp.text}"
    data = resp.json()
    # El modelo Todo devuelve por lo menos {"id":…, …}
    todo_id = data.get("id")
    assert isinstance(todo_id, int), f"ID inválido en la respuesta: {data}"
    return todo_id

