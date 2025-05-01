
set -e

echo "👉 PASO 1: Levanta tu API backend"
echo "   En otra ventana de terminal, ve a la carpeta 'TodoApi' y ejecuta:"
echo "     dotnet run"
echo "   Espera a ver algo como 'Now listening on http://localhost:5141'."
read -p "✅ Cuando tu API esté corriendo en http://localhost:5141, presiona ENTER para continuar..."

echo
echo "👉 PASO 2: Levanta tu frontend"
echo "   En otra terminal, ve a 'todo-client' y ejecuta:"
echo "     npm start"
echo "   Espera a ver 'Local: http://localhost:3000'."
read -p "✅ Cuando tu frontend esté corriendo en http://localhost:3000, presiona ENTER para continuar..."

echo
echo "👉 PASO 3: Ejecutando tests con pytest"
pytest scripts/test_todo_app.py -q --disable-warnings

echo
echo "✅ ¡Todos los tests han pasado!"

