import requests
import pytest

BASE = "http://localhost:5141"

def test_obtener_un_todo_específico_del_usuario_autenticado(auth_headers, initial_todo):
    """Obtener un todo específico del usuario autenticado"""
    
    # Definir un ID válido de ejemplo
    # valid_id = 1
    
    # Construir la URL con ese ID
    url = BASE + f"/api/Todo/{initial_todo}"
    
    # Hacer la petición GET
    r = requests.get(url, headers=auth_headers)

    # Validar el código HTTP
    assert r.status_code == 200, f"Status inesperado: {r.status_code}"

    # Validar que la respuesta sea un dict y que el campo id coincida
    data = r.json()
    assert isinstance(data, dict), "La respuesta no es un objeto JSON"
    # assert data.get("id") == valid_id, f"Se devolvió el todo equivocado: {data}"

def test_crear_un_nuevo_todo_para_el_usuario_autenticado(auth_headers):
    """Crear un nuevo todo para el usuario autenticado"""

    # Construir la URL
    url = BASE + f"/api/Todo"

    # TODO: define payload válido como dict Python
    payload = { # << insertar los campos desde testcases_response.md
        "Title": "Comprar café",
        "IsCompleted": False,
        "Category": "Work"
    }

    # Hacer la petición POST  
    r = requests.post(url, json=payload, headers=auth_headers)

    # Validar el código HTTP
    assert r.status_code == 201, f"Status inesperado: {r.status_code}"

    # Validar la respuesta
    data = r.json()
    assert data is not None

def test_actualizar_un_todo_existente_del_usuario_autenticado(auth_headers, initial_todo):
    """Actualizar un todo existente del usuario autenticado"""
    # Definir un ID válido de ejemplo
    # valid_id = 1
    
    # Construir la URL con ese ID
    url = BASE + f"/api/Todo/{initial_todo}"

    # TODO: define payload válido como dict Python
    payload = { # << insertar los campos desde testcases_response.md
        "Title":       "Tarea Actualizada",  
        "IsCompleted": True,                  
        "Category":    "Work"
    }

    # Enviar la petición PUT con el JSON en el body  
    r = requests.put(url, json=payload, headers=auth_headers)

    # Verificar que el status code sea 200 OK
    assert r.status_code == 200, f"Status inesperado: {r.status_code}"

    # Comprobar que la respuesta devuelva el todo actualizado
    data = r.json()
    assert isinstance(data, dict), "La respuesta no es un objeto JSON"
    # assert data.get("id") == valid_id,           "El ID devuelto no coincide"
    assert data.get("title") == payload["Title"],            "El título no se actualizó"
    assert data.get("isCompleted") == payload["IsCompleted"], "El estado no coincide"
    assert data.get("category") == payload["Category"],      "La categoría no coincide"

def test_eliminar_un_todo_existente_del_usuario_autenticado(auth_headers, initial_todo):
    """Eliminar un todo existente del usuario autenticado"""

    # Definir un ID válido de ejemplo
    # valid_id = 1

    # Construir la URL 
    url = BASE + f"/api/Todo/{initial_todo}"

    # Enviar la petición DELETE
    r = requests.delete(url, headers=auth_headers)

    # Verificar que el código sea 204 No Content   
    assert r.status_code == 204, f"Status inesperado: {r.status_code}"
    
    # Comprobar que el cuerpo venga vacío
    assert r.text == "", "Se esperaba cuerpo vacío tras eliminación"
