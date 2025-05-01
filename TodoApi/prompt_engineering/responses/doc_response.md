El controlador `TodoController` es un controlador de API REST que maneja operaciones CRUD (Crear, Leer, Actualizar, Eliminar) para la entidad `Todo`. Este controlador requiere autenticación para acceder a sus endpoints, lo que significa que solo los usuarios autenticados pueden realizar operaciones en él.

### Endpoints:

1. **GET api/Todo**
   - Tipo de petición: GET
   - Parámetros: Ninguno
   - Respuestas:
     - 200 OK: Devuelve una lista de todos los `Todo` asociados al usuario autenticado.
     - 401 Unauthorized: Si el usuario no está autenticado.
     
2. **GET api/Todo/{id}**
   - Tipo de petición: GET
   - Parámetros: `id` (int)
   - Respuestas:
     - 200 OK: Devuelve el `Todo` con el `id` especificado si pertenece al usuario autenticado.
     - 401 Unauthorized: Si el usuario no está autenticado.
     - 404 Not Found: Si no se encuentra un `Todo` con el `id` especificado para el usuario autenticado.
     
3. **POST api/Todo**
   - Tipo de petición: POST
   - Parámetros: Body con los datos del nuevo `Todo` en formato JSON con los campos `Title`, `IsCompleted` y `Category`.
   - Respuestas:
     - 201 Created: Devuelve el nuevo `Todo` creado.
     - 400 Bad Request: Si los datos enviados no son válidos o faltan campos requeridos.
     - 401 Unauthorized: Si el usuario no está autenticado.
     - 500 Internal Server Error: Si ocurre un error al intentar crear el `Todo`.
     
4. **PUT api/Todo/{id}**
   - Tipo de petición: PUT
   - Parámetros: `id` (int) en la URL y Body con los datos actualizados del `Todo` en formato JSON con los campos `Title`, `IsCompleted` y `Category`.
   - Respuestas:
     - 200 OK: Devuelve el `Todo` actualizado.
     - 400 Bad Request: Si los datos enviados no son válidos o faltan campos requeridos.
     - 401 Unauthorized: Si el usuario no está autenticado.
     - 404 Not Found: Si no se encuentra un `Todo` con el `id` especificado para el usuario autenticado.
     - 500 Internal Server Error: Si ocurre un error al intentar actualizar el `Todo`.
     
5. **DELETE api/Todo/{id}**
   - Tipo de petición: DELETE
   - Parámetros: `id` (int)
   - Respuestas:
     - 204 No Content: Indica que el `Todo` fue eliminado con éxito.
     - 401 Unauthorized: Si el usuario no está autenticado.
     - 404 Not Found: Si no se encuentra un `Todo` con el `id` especificado para el usuario autenticado.

En resumen, este controlador permite a los usuarios autenticados realizar operaciones CRUD en sus `Todo`, incluyendo la creación, lectura, actualización y eliminación de los mismos. Además, valida los datos enviados en las solicitudes y maneja posibles errores de manera adecuada.