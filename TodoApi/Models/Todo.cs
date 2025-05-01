namespace TodoApi.Models
{
    public class Todo
    {
        public int Id { get; set; }
        public required string Title { get; set; }
        public bool IsCompleted { get; set; }
        public DateTime CreatedAt { get; set; }
        public required string Category { get; set; }
        public int UserId { get; set; }
        public User? User { get; set; }
    }

    public static class Categories
    {
        public static readonly string[] DefaultCategories = new[]
        {
            "Work",
            "Personal",
            "Shopping",
            "Health",
            "Important",
            "Study"
        };
    }
}
