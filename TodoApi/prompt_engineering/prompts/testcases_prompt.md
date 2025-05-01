```md
Actúa como ingeniero de calidad de software. A partir del código del controlador de tareas, genera una tabla con al menos 5 casos de prueba. Incluye: ID, nombre del caso, endpoint, método HTTP, entradas válidas, entradas inválidas, salida esperada y estatus esperado.

```csharp
[
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using TodoApi.Data;
using TodoApi.Models;
using Microsoft.AspNetCore.Authorization;

namespace TodoApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class TodoController : ControllerBase
    {
        private readonly TodoDbContext _context;

        public TodoController(TodoDbContext context)
        {
            _context = context;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Todo>>> GetTodos()
        {
            var username = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
            if (username == null)
            {
                return Unauthorized();
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
            if (user == null)
            {
                return Unauthorized();
            }

            return await _context.Todos.Where(t => t.UserId == user.Id).ToListAsync();
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Todo>> GetTodo(int id)
        {
            var username = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
            if (username == null)
            {
                return Unauthorized();
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
            if (user == null)
            {
                return Unauthorized();
            }

            var todo = await _context.Todos.FirstOrDefaultAsync(t => t.Id == id && t.UserId == user.Id);
            if (todo == null)
            {
                return NotFound();
            }
            return todo;
        }

        public record CreateTodoRequest(string Title, bool IsCompleted, string Category);

        [HttpPost]
        public async Task<ActionResult<Todo>> CreateTodo([FromBody] CreateTodoRequest request)
        {
            var username = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
            if (username == null)
            {
                return Unauthorized();
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
            if (user == null)
            {
                return Unauthorized();
            }

            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            if (string.IsNullOrWhiteSpace(request.Title))
            {
                return BadRequest(new { error = "Title is required" });
            }

            if (string.IsNullOrWhiteSpace(request.Category))
            {
                return BadRequest(new { error = "Category is required" });
            }

            if (!Categories.DefaultCategories.Contains(request.Category))
            {
                return BadRequest(new { error = "Invalid category" });
            }

            try
            {
                var todo = new Todo
                {
                    Title = request.Title,
                    IsCompleted = request.IsCompleted,
                    Category = request.Category,
                    CreatedAt = DateTime.UtcNow,
                    UserId = user.Id
                };

                _context.Todos.Add(todo);
                await _context.SaveChangesAsync();

                return CreatedAtAction(nameof(GetTodo), new { id = todo.Id }, todo);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = "Failed to create todo" });
            }
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateTodo(int id, [FromBody] CreateTodoRequest request)
        {
            var username = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
            if (username == null)
            {
                return Unauthorized();
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
            if (user == null)
            {
                return Unauthorized();
            }

            var todo = await _context.Todos.FirstOrDefaultAsync(t => t.Id == id && t.UserId == user.Id);
            if (todo == null)
            {
                return NotFound();
            }

            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            if (string.IsNullOrWhiteSpace(request.Title))
            {
                return BadRequest(new { error = "Title is required" });
            }

            if (string.IsNullOrWhiteSpace(request.Category))
            {
                return BadRequest(new { error = "Category is required" });
            }

            if (!Categories.DefaultCategories.Contains(request.Category))
            {
                return BadRequest(new { error = "Invalid category" });
            }

            todo.Title = request.Title;
            todo.IsCompleted = request.IsCompleted;
            todo.Category = request.Category;

            try
            {
                await _context.SaveChangesAsync();
                return Ok(todo);
            }
            catch (Exception ex)
            {
                return StatusCode(500, new { error = "Failed to update todo" });
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteTodo(int id)
        {
            var username = User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
            if (username == null)
            {
                return Unauthorized();
            }

            var user = await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
            if (user == null)
            {
                return Unauthorized();
            }

            var todo = await _context.Todos.FirstOrDefaultAsync(t => t.Id == id && t.UserId == user.Id);
            if (todo == null)
            {
                return NotFound();
            }

            _context.Todos.Remove(todo);
            await _context.SaveChangesAsync();

            return NoContent();
        }
    }
}
]