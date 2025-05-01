Aquí tienes la tabla en formato Markdown con los casos de prueba que proporcionaste:

```markdown
| ID    | Título                     | Precondición                     | Pasos                                                        | Resultado Esperado                                          |
|-------|----------------------------|----------------------------------|--------------------------------------------------------------|-----------------------------------------------------------|
| TC-01 | Inicio de sesión válido     | App en pantalla de Login         | Visitar Login; Ingresar credenciales válidas; Clic en Login | Usuario redirigido a lista de tareas y token guardado en localStorage |
| TC-02 | Inicio de sesión inválido   | App en pantalla de Login         | Visitar Login; Ingresar credenciales inválidas; Clic en Login | Mensaje de error y permanece en Login                      |
| TC-03 | Registro de nuevo usuario    | App en pantalla de Login         | Clic en Register; Ingresar datos de usuario; Clic en Register | Usuario nuevo creado y redirigido a lista de tareas       |
| TC-04 | Toggle Dark Mode            | Usuario autenticado en TodoList | Clic en toggle de tema                                       | UI cambia entre modo claro y oscuro                        |
| TC-05 | Cerrar sesión               | Usuario autenticado en TodoList | Clic en botón Logout                                         | Redirige a Login y limpia localStorage                     |
| TC-06 | Persistencia tras recarga   | Usuario autenticado              | Recargar la página                                          | Permanece en TodoList sin pedir login                      |
```

Puedes copiar y pegar este código en cualquier editor que soporte Markdown para visualizar la tabla correctamente.