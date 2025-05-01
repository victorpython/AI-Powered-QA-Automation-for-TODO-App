# Todo Application with Authentication

A full-stack todo application built with ASP.NET Core and React, featuring user authentication and a modern Material-UI interface.

## Features

- User authentication (register/login)
- JWT-based authentication
- CRUD operations for todos
- Category-based todo organization
- Dark/Light mode theme switching
- Import/Export todos (JSON/CSV)
- Modern, responsive UI with Material-UI
- Secure password hashing with BCrypt

## Tech Stack

### Backend (.NET 7)
- ASP.NET Core Web API
- Entity Framework Core with SQLite
- JWT Authentication
- BCrypt.Net for password hashing
- CORS enabled for frontend communication

### Frontend (React)
- TypeScript
- Material-UI components
- React Hooks
- Axios for API communication
- Local storage for auth persistence

## Getting Started

### Prerequisites
- .NET 7 SDK
- Node.js and npm
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd WindNetDemo
```

2. Start the backend:
```bash
cd TodoApi
dotnet run
```
The API will be available at `http://localhost:5141`

3. Start the frontend:
```bash
cd todo-client
npm install
npm start
```
The React app will be available at `http://localhost:3001`

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register a new user
- POST `/api/auth/login` - Login and get JWT token

### Todos
- GET `/api/todo` - Get all todos for authenticated user
- GET `/api/todo/{id}` - Get specific todo
- POST `/api/todo` - Create new todo
- PUT `/api/todo/{id}` - Update todo
- DELETE `/api/todo/{id}` - Delete todo

## Frontend Features

### Authentication
- User registration with username/password
- Login with username/password
- Automatic token refresh
- Secure token storage

### Todo Management
- Create, read, update, and delete todos
- Filter todos by category
- Mark todos as complete/incomplete
- Import/Export functionality
- Dark/Light mode theme

## Security Features

- Password hashing using BCrypt
- JWT token authentication
- Protected API endpoints
- CORS configuration
- User-specific todo access

## Project Structure

```
WindNetDemo/
├── TodoApi/                # Backend API
│   ├── Controllers/        # API endpoints
│   ├── Models/            # Data models
│   ├── Data/              # Database context
│   └── Program.cs         # App configuration
│
└── todo-client/           # Frontend React app
    ├── src/
    │   ├── components/    # React components
    │   ├── types/        # TypeScript types
    │   └── App.tsx       # Main app component
    └── package.json      # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## License

This project is licensed under the MIT License.
